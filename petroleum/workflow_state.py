from dataclasses import dataclass, field
from typing import List, Optional
from petroleum.task_log import TaskLogEntry
from petroleum.workflow_status import WorkflowStatus


@dataclass
class WorkflowState:
    next_task_id: Optional[str]
    task_log: List[TaskLogEntry] = field(default_factory=list)
    status_log: List[WorkflowStatus] = field(default_factory=list)
