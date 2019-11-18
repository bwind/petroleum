from dataclasses import dataclass, field
from typing import Any


__all__ = ["WorkflowStatus", "WorkflowStatusEnum"]


class WorkflowStatusEnum:
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"
    FAILED = "FAILED"


@dataclass
class WorkflowStatus:
    status: str
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    exception: Any = None
