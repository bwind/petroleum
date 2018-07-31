from expects import expect, equal, raise_error
from mamba import before, context, description, it
from petroleum import Task, Workflow, WorkflowStatus


with description('task'):
    with it('can instantiate without arguments'):
        expect(lambda: Task()).not_to(raise_error(Exception))

    with it('accepts arbitrary keyword arguments as task data'):
        task = Task(foo='bar')
        expect(task.foo).to(equal('bar'))


with description('workflow') as self:
    with before.each:
        self.task = Task()
        self.workflow = Workflow(start_task=self.task)

    with context('when resuming'):
        with it('accepts arbitrary keyword arguments as inputs'):
            self.workflow.resume(foo='bar')

    with context('when task is not ready'):
        with before.each:
            self.task.is_ready = lambda **i: False

        with it('returns suspended workflow status'):
            workflow_status = self.workflow.start()
            expect(workflow_status.status).to(equal(WorkflowStatus.SUSPENDED))

        with it('returns workflow status with task inputs'):
            inputs = {'foo': 'bar'}
            workflow_status = self.workflow.start(**inputs)
            expect(workflow_status.inputs).to(equal(inputs))


with description('workflow data') as self:
    with before.each:
        self.task = Task()
        self.workflow = Workflow(foo='bar', start_task=self.task)
        self.workflow.start()

    with it('has access to workflow data'):
        expect(self.task.workflow_data['foo']).to(equal('bar'))

    with it('modifies workflow data'):
        self.task.workflow_data['foo'] = 'baz'
        expect(self.workflow.workflow_data['foo']).to(equal('baz'))


with description('json encoder'):
    with context('task.to_json'):
        with it('returns json'):
            expect(Task().to_json()).to(equal(
                '{"name": null, "next_task": null}'))

    with context('workflow.to_json'):
        with it('returns json'):
            start_task = Task()
            expect(Workflow(start_task=start_task).to_json()).to(equal(
                '{"current_task": {"name": null, "next_task": null}, "start_task": {"name": null, "next_task": null}, "workflow_data": {}}'))  # noqa: E501
