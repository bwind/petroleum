from dataclasses import dataclass

from petroleum.json_encoder import ToJSONMixin
from petroleum.task_status import TaskStatus, TaskStatusEnum


@dataclass
class Task(ToJSONMixin):
    id: str = None
    name: str = None
    task_data: dict = None
    next_task: str = None

    def _run(self, **inputs):
        if not self.is_ready(**inputs):
            return TaskStatus(status=TaskStatusEnum.WAITING, inputs=inputs)
        try:
            outputs = self.run(**inputs)
        except Exception as exc:
            return TaskStatus(
                status=TaskStatusEnum.FAILED, exception=exc, inputs=inputs
            )
        task_result = TaskStatus(
            status=TaskStatusEnum.COMPLETED, inputs=inputs, outputs=outputs
        )
        self.on_complete(task_result)
        return task_result

    def connect(self, task):
        self.next_task = task.id
        self._next_task = task

    def get_next_task(self, task_status):
        return getattr(self, "_next_task", None)

    def is_ready(self, **inputs):
        return True

    def on_complete(self, task_result):
        pass

    def run(self, **inputs):
        raise NotImplementedError()
