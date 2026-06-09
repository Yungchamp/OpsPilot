from opspilot.storage.migrations import run_migrations
from opspilot.storage.repositories import JobRepository


def test_jobs_retry(tmp_path):
    db = tmp_path / 'j.db'
    run_migrations(str(db))
    repo = JobRepository(db_path=str(db))
    job = {'job_id':'J1','job_type':'escalate','payload':{'incident_id':'x'},'status':'queued','attempts':0}
    repo.insert(job)
    nxt = repo.next_job()
    assert nxt['job_id']=='J1'
    repo.mark_failed('J1','err')
    f = repo.next_job()
    assert f is None
