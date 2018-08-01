from petroleum import PetroleumObject
from petroleum.json_encoder import ToJSONMixin
from petroleum.task_status import TaskStatus


class Task(PetroleumObject, ToJSONMixin):
    def __init__(self, name=None, **task_data):
        self.name = name
        self.next_task = None
        self.__dict__.update(task_data)

    def __repr__(self):
        return '<%s (%s)>' % (self.__class__.__name__, self.name)

    def _run(self, **inputs):
        if not self.is_ready(**inputs):
            return TaskStatus(status=TaskStatus.WAITING, inputs=inputs)
        try:
            outputs = self.run(**inputs)
        except Exception as exc:
            return TaskStatus(status=TaskStatus.FAILED,
                              exception=exc,
                              inputs=inputs)
        task_result = TaskStatus(status=TaskStatus.COMPLETED,
                                 inputs=inputs,
                                 outputs=outputs)
        self.on_complete(task_result)
        return task_result

    def connect(self, task):
        self.next_task = task

    def get_next_task(self, task_status):
        return self.next_task

    def is_ready(self, **inputs):
        return True

    def on_complete(self, task_result):
        pass

    def run(self, **inputs):
        pass
