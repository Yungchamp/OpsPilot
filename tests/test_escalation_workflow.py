import tempfile
from datetime import datetime, timedelta
from opspilot.storage.migrations import run_migrations
from opspilot.services.incident_service import IncidentService
from opspilot.services.escalation_service import EscalationService
from opspilot.services.notification_service import NotificationService
from opspilot.services.analytics_service import AnalyticsService
from opspilot.storage.repositories import JobRepository, IncidentRepository


def test_critical_incident_creates_escalation(tmp_path):
    db = tmp_path / 'e.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))

    inc = {'incident_id':'INC-001','title':'Critical outage','description':'database down','severity':'critical','service':'orders'}
    inc_svc.create(inc)

    result = esc_svc.create_for_incident('INC-001')
    assert result['escalation']['incident_id'] == 'INC-001'
    assert result['escalation']['status'] == 'pending'
    assert result['escalation']['assigned_team'] == 'oncall'
    assert result['notification_payload']['incident_id'] == 'INC-001'
    assert result['notification_payload']['priority'] == 'high'


def test_resolved_incident_does_not_create_escalation(tmp_path):
    db = tmp_path / 'e2.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))

    inc = {'incident_id':'INC-010','title':'Fixed error','description':'service recovered','severity':'critical','service':'payments'}
    inc_svc.create(inc)
    inc_svc.transition('INC-010', 'triaging')
    inc_svc.transition('INC-010', 'investigating')
    inc_svc.transition('INC-010', 'mitigated')
    inc_svc.transition('INC-010', 'resolved')

    try:
        esc_svc.create_for_incident('INC-010')
        assert False, 'should not escalate resolved incident'
    except ValueError as exc:
        assert 'resolved incidents' in str(exc)


def test_duplicate_active_escalation_is_prevented(tmp_path):
    db = tmp_path / 'e3.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))

    inc = {'incident_id':'INC-020','title':'Latency spike','description':'timeout errors','severity':'critical','service':'checkout'}
    inc_svc.create(inc)
    esc_svc.create_for_incident('INC-020')
    try:
        esc_svc.create_for_incident('INC-020')
        assert False, 'duplicate active escalation should be blocked'
    except ValueError as exc:
        assert 'active escalation exists' in str(exc)


def test_high_risk_unresolved_incident_escalates_after_threshold(tmp_path):
    db = tmp_path / 'e4.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))
    repo = IncidentRepository(db_path=str(db))

    inc = {'incident_id':'INC-030','title':'High risk alert','description':'disk pressure','severity':'high','service':'billing'}
    inc_svc.create(inc)
    incident = repo.get('INC-030')
    incident['risk_score'] = 0.8
    incident['created_at'] = (datetime.utcnow() - timedelta(minutes=120)).isoformat() + 'Z'
    repo.update('INC-030', incident)

    result = esc_svc.create_for_incident('INC-030')
    assert result['escalation']['severity'] == 'high'
    assert 'high-risk incident' in result['escalation']['reason']


def test_notification_payload_is_deterministic(tmp_path):
    payload = NotificationService().prepare_escalation_payload({
        'escalation_id': 'ESC-ABC',
        'incident_id': 'INC-050',
        'severity': 'critical',
        'assigned_team': 'oncall',
        'reason': 'critical incident requires immediate escalation',
        'notification_targets': ['oncall@ops.example.com']
    })
    assert payload['target'] == 'oncall@ops.example.com'
    assert payload['channel'] == 'email'
    assert payload['incident_id'] == 'INC-050'
    assert payload['escalation_id'] == 'ESC-ABC'
    assert 'Escalation ESC-ABC for incident INC-050' in payload['subject']


def test_notification_job_is_queued_with_idempotency_key(tmp_path):
    db = tmp_path / 'e5.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))
    repo = JobRepository(db_path=str(db))

    inc = {'incident_id':'INC-060','title':'Backend error','description':'panic','severity':'critical','service':'api'}
    inc_svc.create(inc)
    esc_svc.create_for_incident('INC-060')

    job = repo.next_job()
    assert job is not None
    assert job['job_type'] == 'escalation_notification'
    assert job['idempotency_key'].startswith('notification:')
    assert job['payload']['incident_id'] == 'INC-060'


def test_acknowledge_and_resolve_status_transitions_work(tmp_path):
    db = tmp_path / 'e6.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))

    inc = {'incident_id':'INC-070','title':'Service degradation','description':'slow responses','severity':'critical','service':'search'}
    inc_svc.create(inc)
    result = esc_svc.create_for_incident('INC-070')
    esc_id = result['escalation']['escalation_id']

    ack = esc_svc.acknowledge(esc_id)
    assert ack['status'] == 'acknowledged'
    assert ack['acknowledged_at'] is not None

    res = esc_svc.resolve(esc_id)
    assert res['status'] == 'resolved'
    assert res['resolved_at'] is not None


def test_analytics_summary_includes_escalation_counts(tmp_path):
    db = tmp_path / 'e7.db'
    run_migrations(str(db))
    inc_svc = IncidentService(db_path=str(db))
    esc_svc = EscalationService(db_path=str(db))
    analytics_svc = AnalyticsService(db_path=str(db))

    inc = {'incident_id':'INC-080','title':'API failure','description':'time out','severity':'critical','service':'gateway'}
    inc_svc.create(inc)
    esc_svc.create_for_incident('INC-080')

    summary = analytics_svc.summary()
    assert 'escalation_health' in summary
    assert summary['escalation_health']['open_escalations'] == 1
    assert summary['escalation_health']['open_escalations_by_severity']['critical'] == 1
    assert summary['escalation_health']['services_with_most_escalations']['gateway'] == 1
