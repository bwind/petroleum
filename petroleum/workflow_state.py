from dataclasses import dataclass, field
from typing import List
from petroleum.task_log import TaskLogEntry


@dataclass
class WorkflowState:
    next_task_id: str
    task_log: List[TaskLogEntry] = field(default_factory=list)
