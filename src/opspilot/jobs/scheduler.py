from ..jobs.queue import JobQueue
from ..services.workflow_service import WorkflowService

class Scheduler:
    def __init__(self, db_path: str | None = None):
        self.queue = JobQueue(db_path=db_path)
        self.workflow = WorkflowService(db_path=db_path)

    def run_once(self):
        return self.workflow.run_once()
