from petroleum.task_status import TaskStatus
from petroleum.workflow_status import WorkflowStatus
import copy


class Workflow:
    def __init__(self, start_task, **workflow_data):
        self.start_task = start_task
        self.current_task = self.start_task
        self.workflow_data = workflow_data

    def _run_tasks(self, task, inputs):
        self.current_task = task
        # Create a copy of this Workflow's workflow_data to avoid Tasks
        # modifying workflow data
        task.workflow_data = copy.deepcopy(self.workflow_data)
        task_status = task._run(inputs)
        if task_status.status == TaskStatus.COMPLETED:
            if task.get_next_task(task_status.outputs) is None:
                return WorkflowStatus(status=WorkflowStatus.COMPLETED,
                                      outputs=task_status.outputs)
            else:
                return self._run_tasks(task.get_next_task(task_status.outputs),
                                       inputs=task_status.outputs)
        elif task_status.status == TaskStatus.FAILED:
            return WorkflowStatus(status=WorkflowStatus.FAILED,
                                  exception=task_status.exception)
        elif task_status.status == TaskStatus.WAITING:
            return WorkflowStatus(status=WorkflowStatus.SUSPENDED,
                                  inputs=task_status.inputs)

    def restart(self, inputs=None):
        return self.start(inputs)

    def resume(self, inputs=None):
        return self._run_tasks(self.current_task, inputs)

    def start(self, inputs=None):
        return self._run_tasks(self.start_task, inputs)
