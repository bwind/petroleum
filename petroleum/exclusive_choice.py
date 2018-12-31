from petroleum.conditional_task import ConditionalTask
from petroleum.exceptions import PetroleumException
from petroleum.task import Task


class ExclusiveChoice(Task):
    def __init__(self, name=None, *args, **kwargs):
        self._conditional_tasks = []
        super().__init__(name=None, *args, **kwargs)

    def get_next_task(self, task_status):
        for conditional_task in self._conditional_tasks:
            result = conditional_task.condition(task_status)
            if not isinstance(result, bool):
                raise PetroleumException('Condition %s did not return bool' %
                                         conditional_task.condition)
            if result is True:
                return conditional_task.task
        return self._next_task

    def connect_if(self, task, condition):
        conditional_task = ConditionalTask(task=task, condition=condition)
        self._conditional_tasks.append(conditional_task)
