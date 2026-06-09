from ..storage.repositories import IncidentRepository, DeploymentRepository, LogRepository
from datetime import datetime

class AnalyticsService:
    def __init__(self, db_path: str | None = None):
        self.inc_repo = IncidentRepository(db_path=db_path)
        self.dep_repo = DeploymentRepository(db_path=db_path)
        self.log_repo = LogRepository(db_path=db_path)

    def summary(self):
        incidents = self.inc_repo.list_all()
        deployments = self.dep_repo.list_all()
        logs = self.log_repo.list_all(limit=100)
        # simple summaries
        open_by_sev = {}
        for inc in incidents:
            if inc['status'] != 'resolved' and inc['status'] != 'closed':
                open_by_sev.setdefault(inc['severity'], 0)
                open_by_sev[inc['severity']] += 1
        dep_stats = {}
        for d in deployments:
            dep_stats.setdefault(d['service'], {'succeeded':0,'failed':0})
            dep_stats[d['service']].setdefault(d['status'],0)
            dep_stats[d['service']][d['status']] = dep_stats[d['service']].get(d['status'],0) + 1
        return {'open_by_severity': open_by_sev, 'deployment_stats': dep_stats, 'recent_logs': logs}
