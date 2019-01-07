from datetime import datetime
from dataclasses import dataclass
from task_status import TaskStatus


@dataclass
class TaskLogEntry:
    id: str
    started_at: datetime
    ended_at: datetime
    status: TaskStatus

    def _update_with_status(self, status):
        self.ended_at = datetime.now()
        self.status = status
