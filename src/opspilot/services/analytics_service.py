from ..storage.repositories import IncidentRepository, DeploymentRepository, LogRepository, EscalationRepository
from datetime import datetime

class AnalyticsService:
    def __init__(self, db_path: str | None = None):
        self.inc_repo = IncidentRepository(db_path=db_path)
        self.dep_repo = DeploymentRepository(db_path=db_path)
        self.log_repo = LogRepository(db_path=db_path)
        self.esc_repo = EscalationRepository(db_path=db_path)

    def summary(self):
        incidents = self.inc_repo.list_all()
        deployments = self.dep_repo.list_all()
        logs = self.log_repo.list_all(limit=100)
        escalations = self.esc_repo.list_all()
        # simple summaries
        open_by_sev = {}
        for inc in incidents:
            if inc['status'] not in ('resolved','closed'):
                open_by_sev.setdefault(inc['severity'], 0)
                open_by_sev[inc['severity']] += 1
        dep_stats = {}
        for d in deployments:
            dep_stats.setdefault(d['service'], {'succeeded':0,'failed':0})
            dep_stats[d['service']].setdefault(d['status'],0)
            dep_stats[d['service']][d['status']] = dep_stats[d['service']].get(d['status'],0) + 1
        open_escalations = [e for e in escalations if e['status'] in ('pending','notified','acknowledged')]
        severity_counts = {}
        for e in open_escalations:
            severity_counts.setdefault(e['severity'], 0)
            severity_counts[e['severity']] += 1
        oldest_pending = None
        pending_list = [e for e in escalations if e['status'] == 'pending']
        if pending_list:
            oldest_pending = min(pending_list, key=lambda x: x['created_at'])
        service_counts = {}
        for e in escalations:
            service_counts[e.get('service') or 'unknown'] = service_counts.get(e.get('service') or 'unknown', 0) + 1
        return {
            'open_by_severity': open_by_sev,
            'deployment_stats': dep_stats,
            'recent_logs': logs,
            'escalation_health': {
                'open_escalations': len(open_escalations),
                'open_escalations_by_severity': severity_counts,
                'oldest_pending_escalation': oldest_pending,
                'services_with_most_escalations': service_counts
            }
        }
