from dataclasses import dataclass, field
from typing import Any


class TaskStatusEnum:
    WAITING = 'WAITING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


@dataclass
class TaskStatus:
    status: str
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    exception: Any = None  # noqa: E701

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.status)
