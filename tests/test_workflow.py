from petroleum import Task, Workflow


class TestWorkflow:
    def setup(self):
        class TestTask(Task):
            def run(self):
                pass

        self.tasks = {
            "a": TestTask(id="a"),
            "b": TestTask(id="b"),
        }
        self.tasks["a"].connect(self.tasks["b"])
        self.id_to_task_mapper = lambda id: self.tasks[id]
        self.workflow = Workflow(
            start_task=self.tasks["a"],
            id_to_task_mapper=self.id_to_task_mapper,
        )

    def test_workflow_stores_completed_state(self):
        assert self.workflow.is_completed() is False
        state = self.workflow.get_state()
        workflow = Workflow(
            start_task=self.tasks["a"],
            id_to_task_mapper=self.id_to_task_mapper,
            state=state,
        )
        assert workflow.is_completed() is False

        self.workflow.start()
        assert self.workflow.is_completed() is True
        state = self.workflow.get_state()
        workflow = Workflow(
            start_task=self.tasks["a"],
            id_to_task_mapper=self.id_to_task_mapper,
            state=state,
        )
        assert workflow.is_completed() is True
