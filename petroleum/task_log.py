from datetime import datetime
from dataclasses import dataclass
from petroleum.task_status import TaskStatus


@dataclass
class TaskLogEntry:
    id: str
    started_at: datetime
    ended_at: datetime = None
    status: TaskStatus = None

    def _update_with_status(self, status):
        self.ended_at = datetime.now()
        self.status = status
