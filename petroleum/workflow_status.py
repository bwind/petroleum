from dataclasses import dataclass


@dataclass
class WorkflowStatus:
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"
    FAILED = "FAILED"

    status: str
    inputs: dict = None
    outputs: dict = None
    exception: object = None
