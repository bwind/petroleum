from petroleum.task_status import TaskStatus
from petroleum.workflow_status import WorkflowStatus
import logging


class Workflow:
    def __init__(self, start_task, **workflow_data):
        self.start_task = start_task
        self.current_task = self.start_task
        self.workflow_data = workflow_data

    def _run_tasks(self, task, **inputs):
        self.current_task = task
        task.workflow_data = self.workflow_data
        logging.warn('Calling %s._run() with inputs %s' % (
            task.__class__.__name__, inputs))
        task_status = task._run(**inputs)
        logging.warn('Outputs: %s' % task_status.outputs)
        if task_status.status == TaskStatus.COMPLETED:
            next_task = task.get_next_task(task_status)
            if next_task is None:
                return WorkflowStatus(status=WorkflowStatus.COMPLETED,
                                      outputs=task_status.outputs)
            else:
                return self._run_tasks(next_task, **task_status.outputs)
        elif task_status.status == TaskStatus.FAILED:
            return WorkflowStatus(status=WorkflowStatus.FAILED,
                                  exception=task_status.exception)
        elif task_status.status == TaskStatus.WAITING:
            return WorkflowStatus(status=WorkflowStatus.SUSPENDED,
                                  inputs=task_status.inputs)

    def restart(self, **inputs):
        return self.start(**inputs)

    def resume(self, **inputs):
        return self._run_tasks(self.current_task, **inputs)

    def start(self, **inputs):
        return self._run_tasks(self.start_task, **inputs)
