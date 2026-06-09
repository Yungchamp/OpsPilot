import argparse
import sys
from .storage import migrations, seed
from .database import get_conn
from .config import settings
from .services.ai_service import AIService
from .services.escalation_service import EscalationService
from .storage.repositories import JobRepository


def cmd_health(args):
    print('OK')


def cmd_seed(args):
    db = args.db or settings.DB_PATH
    migrations.run_migrations(db)
    seed.seed_demo(db)
    print('seed done')


def cmd_ingest_logs(args):
    from .services.log_ingestion_service import LogIngestionService
    db = args.db or settings.DB_PATH
    svc = LogIngestionService(db_path=db)
    svc.ingest_file(args.file)
    print('ingested', args.file)


def cmd_triage(args):
    svc = AIService()
    report = svc.triage(args.incident)
    print(report)


def cmd_report(args):
    print('report: not implemented')


def cmd_escalations(args):
    db = args.db or settings.DB_PATH
    svc = EscalationService(db_path=db)
    for esc in svc.list():
        print(esc['escalation_id'], esc['incident_id'], esc['status'], esc['severity'])


def cmd_escalate(args):
    db = args.db or settings.DB_PATH
    svc = EscalationService(db_path=db)
    result = svc.create_for_incident(args.incident)
    print(result)


def cmd_pending_notifications(args):
    db = args.db or settings.DB_PATH
    repo = JobRepository(db_path=db)
    job = repo.next_job()
    if not job:
        print('no pending notifications')
        return
    print(job['job_id'], job['job_type'], job.get('idempotency_key'), job['payload'].get('incident_id'))


def main():
    parser = argparse.ArgumentParser(prog='opspilot')
    sub = parser.add_subparsers()

    p = sub.add_parser('health')
    p.set_defaults(func=cmd_health)

    p = sub.add_parser('seed')
    p.add_argument('--db')
    p.set_defaults(func=cmd_seed)

    p = sub.add_parser('ingest-logs')
    p.add_argument('--db')
    p.add_argument('--file', required=True)
    p.set_defaults(func=cmd_ingest_logs)

    p = sub.add_parser('triage')
    p.add_argument('--db')
    p.add_argument('--incident', required=True)
    p.set_defaults(func=cmd_triage)

    p = sub.add_parser('escalations')
    p.add_argument('--db')
    p.set_defaults(func=cmd_escalations)

    p = sub.add_parser('escalate')
    p.add_argument('--db')
    p.add_argument('--incident', required=True)
    p.set_defaults(func=cmd_escalate)

    p = sub.add_parser('pending-notifications')
    p.add_argument('--db')
    p.set_defaults(func=cmd_pending_notifications)

    p = sub.add_parser('report')
    p.set_defaults(func=cmd_report)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
