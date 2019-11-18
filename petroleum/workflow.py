from datetime import datetime
from dataclasses import asdict, dataclass

from dacite import from_dict

from petroleum.exceptions import WorkflowRecursionError
from petroleum.json_encoder import ToJSONMixin
from petroleum.task_status import TaskStatusEnum
from petroleum.workflow_status import WorkflowStatus, WorkflowStatusEnum
from petroleum.task_log import TaskLogEntry
from petroleum.workflow_state import WorkflowState


MAX_RECURSION_DEPTH = 5


@dataclass
class Workflow(ToJSONMixin):
    start_task: object
    id_to_task_mapper: object
    task_to_id_mapper: object = None
    state: object = None

    def __init__(
        self, start_task, id_to_task_mapper, task_to_id_mapper=None, state=None
    ):
        """Constructor for a Petroleum workflow

        :param start_task: The start_task object for the workflow
        :param id_to_task_mapper: A function which maps an id to a task
        :param task_to_id_mapper: A function which maps a task to its id
                                 (optional, default is `task.id`)
        :param state: Existing state from a suspended workflow, if any
        """
        self.start_task = start_task
        self.id_to_task_mapper = id_to_task_mapper
        self.task_to_id_mapper = task_to_id_mapper or (lambda task: task.id)
        self._init_state(state)

    def __eq__(self, other):
        return (
            self.start_task == other.start_task and self.state == other.state
        )

    def _init_state(self, state):
        state = state or {}
        if "next_task_id" not in state:
            state["next_task_id"] = self.task_to_id_mapper(self.start_task)
        self.state = from_dict(data_class=WorkflowState, data=state)

    def _run_with_log(self, task, inputs):
        log_entry = TaskLogEntry(
            started_at=datetime.now(), id=self.task_to_id_mapper(task)
        )
        self.state.task_log.append(log_entry)
        task_status = task._run(**inputs)
        log_entry._update_with_status(task_status)
        return task_status

    def _return_workflow_status(self, workflow_status):
        self.state.status_log.append(workflow_status)
        return workflow_status

    def _run_tasks(self, task, **inputs):
        if not hasattr(self, "_recursion_log"):
            self._recursion_log = []
        if self._recursion_log.count(task.id) >= MAX_RECURSION_DEPTH:
            return self._return_workflow_status(
                WorkflowStatus(
                    status=WorkflowStatusEnum.FAILED,
                    exception=WorkflowRecursionError(
                        f"Maximum recursion depth "
                        f"({MAX_RECURSION_DEPTH}) exceeded"
                    ),
                )
            )
        self._recursion_log.append(task.id)
        self.current_task = task
        task_status = self._run_with_log(task, inputs)
        if task_status.status == TaskStatusEnum.COMPLETED:
            next_task = task.get_next_task(task_status)
            if next_task is None:
                return self._return_workflow_status(
                    WorkflowStatus(
                        status=WorkflowStatusEnum.COMPLETED,
                        outputs=task_status.outputs,
                    )
                )
            else:
                self.state.next_task_id = self.task_to_id_mapper(next_task)
                return self._run_tasks(next_task, **task_status.outputs or {})
        elif task_status.status == TaskStatusEnum.FAILED:
            return self._return_workflow_status(
                WorkflowStatus(
                    status=WorkflowStatusEnum.FAILED,
                    exception=task_status.exception,
                )
            )
        elif task_status.status == TaskStatusEnum.WAITING:
            return self._return_workflow_status(
                WorkflowStatus(
                    status=WorkflowStatusEnum.SUSPENDED,
                    inputs=task_status.inputs,
                )
            )

    def _get_next_task(self):
        return self.id_to_task_mapper(self.state.next_task_id)

    def is_completed(self):
        if self.state.status_log:
            return (
                self.state.status_log[-1].status
                == WorkflowStatusEnum.COMPLETED
            )
        return False

    def get_state(self) -> dict:
        return asdict(self.state)

    def resume(self, **inputs):
        if self.is_completed():
            return
        if len(self.state.task_log) > 0:
            inputs = {**self.state.task_log[-1].status.inputs, **inputs}
        return self._run_tasks(self._get_next_task(), **inputs)

    def start(self, **inputs):
        return self.resume(**inputs)
