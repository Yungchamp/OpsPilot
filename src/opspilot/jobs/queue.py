from ..storage.repositories import JobRepository

class JobQueue:
    def __init__(self, db_path: str | None = None):
        self.repo = JobRepository(db_path=db_path)

    def enqueue(self, job):
        self.repo.insert(job)

    def next(self):
        return self.repo.next_job()
