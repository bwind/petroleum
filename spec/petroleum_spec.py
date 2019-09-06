from expects import expect, equal, raise_error
from mamba import before, context, description, it
from petroleum import Task, Workflow, ExclusiveChoice, WorkflowStatus


with description("task"):
    with it("can instantiate without arguments"):
        expect(lambda: Task()).not_to(raise_error(Exception))

    with it("accepts task data"):
        task = Task(task_data={"foo": "bar"})
        expect(task.task_data["foo"]).to(equal("bar"))

    with it("equals to another task"):
        expect(Task(id="bar")).to(equal(Task(id="bar")))

    with it("differs from another task"):
        expect(Task(id="bar")).not_to(equal(Task(id="X")))


with description("workflow") as self:
    with before.each:
        self.task = Task()
        self.workflow = Workflow(
            start_task=self.task,
            task_to_id_mapper=lambda task: "task_id",
            id_to_task_mapper=lambda task_id: self.task,
        )

    with it("equals to another workflow"):
        workflow1 = Workflow(
            start_task=self.task,
            task_to_id_mapper=None,
            id_to_task_mapper=None,
        )
        workflow2 = Workflow(
            start_task=self.task,
            task_to_id_mapper=None,
            id_to_task_mapper=None,
        )
        expect(workflow1).to(equal(workflow2))

    with it("differs from another workflow"):
        expect(self.workflow).not_to(
            equal(
                Workflow(
                    start_task=self.task, id_to_task_mapper=lambda foo: foo
                )
            )
        )

    with context("when resuming"):
        with it("accepts arbitrary keyword arguments as inputs"):
            self.workflow.resume(foo="bar")

    with context("when task is not ready"):
        with before.each:
            self.task.is_ready = lambda **i: False

        with it("returns suspended workflow status"):
            workflow_status = self.workflow.start()
            expect(workflow_status.status).to(equal(WorkflowStatus.SUSPENDED))

        with it("returns workflow status with task inputs"):
            inputs = {"foo": "bar"}
            workflow_status = self.workflow.start(**inputs)
            expect(workflow_status.inputs).to(equal(inputs))


with description("json encoder"):
    with context("task.to_json"):
        with it("returns json"):
            expect(Task().to_json()).to(
                equal(
                    '{"id": null, "name": null, "next_task": null, "task_data": null}'  # noqa: E501
                )
            )


with description("workflow state"):
    with context("workflow.get_state"):
        with it("returns state"):
            start_task = Task()
            expect(
                Workflow(
                    start_task=start_task,
                    task_to_id_mapper=lambda task: "id",
                    id_to_task_mapper=lambda id: start_task,
                ).get_state()
            ).to(equal({"task_log": [], "next_task_id": "id"}))

with description("resume with inputs"):
    with before.each:
        start_task = ExclusiveChoice()
        next_task = Task()

        self.tasks = {"start_task": start_task, "next_task": next_task}

        for task in self.tasks.values():
            task.run = lambda **args: {"success": True}
        self.tasks["next_task"].is_ready = lambda **args: False

        def task_to_id_mapper(task):
            for k, v in self.tasks.items():
                if v == task:
                    return k

        start_task.connect_if(next_task, lambda *args: False)

        self.workflow = Workflow(
            start_task=start_task,
            task_to_id_mapper=task_to_id_mapper,
            id_to_task_mapper=lambda task_id: self.tasks[task_id],
        )

    with it("resubmits inputs"):
        self.workflow.start(example_input="foo")
        self.workflow.resume()

        expect(self.workflow.state.task_log[-1].status.inputs).to(
            equal({"example_input": "foo"})
        )

with description("run workflow"):
    with before.each:
        start_task = Task()
        next_task = ExclusiveChoice()
        another_task = Task()

        self.tasks = {
            "start_task": start_task,
            "next_task": next_task,
            "another_task": another_task,
        }

        def task_to_id_mapper(task):
            for k, v in self.tasks.items():
                if v == task:
                    return k

        start_task.connect(next_task)
        next_task.connect_if(another_task, lambda *args: False)

        self.workflow = Workflow(
            start_task=start_task,
            task_to_id_mapper=task_to_id_mapper,
            id_to_task_mapper=lambda task_id: self.tasks[task_id],
        )

    with context("workflow.get_state 2"):
        with before.each:
            for task in self.tasks.values():
                task.run = lambda **args: {"success": True}
            self.tasks["next_task"].is_ready = lambda **args: False
        with it("returns state"):
            status = self.workflow.start()

            expect(status.status).to(equal(WorkflowStatus.SUSPENDED))

            state = self.workflow.get_state()
            expect(len(state["task_log"])).to(equal(2))
            expect(state["next_task_id"]).to(equal("next_task"))

            self.tasks["next_task"].is_ready = lambda **args: True

            # Create a new workflow
            workflow = Workflow(
                start_task=self.workflow.start_task,
                task_to_id_mapper=self.workflow.task_to_id_mapper,
                id_to_task_mapper=lambda task_id: self.tasks[task_id],
                state=state,
            )
            expect(len(workflow.state.task_log)).to(equal(2))

            status = workflow.resume()
            expect(status.status).to(equal(WorkflowStatus.COMPLETED))
            expect(len(workflow.state.task_log)).to(equal(3))
