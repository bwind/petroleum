from expects import expect, equal, raise_error
from mamba import before, description, it
from petroleum import Task, Workflow


with description('task'):
    with it('can instantiate without arguments'):
        expect(lambda: Task()).not_to(raise_error(Exception))

    with it('accepts arbitrary keyword arguments as task data'):
        task = Task(foo='bar')
        expect(task.foo).to(equal('bar'))


with description('workflow data') as self:
    with before.each:
        self.task = Task()
        self.workflow = Workflow(foo='bar', start_task=self.task)
        self.workflow.start()

    with it('has access to workflow data'):
        expect(self.task.workflow_data['foo']).to(equal('bar'))

    with it('does not modify workflow data'):
        self.task.workflow_data['foo'] = 'baz'
        expect(self.workflow.workflow_data['foo']).to(equal('bar'))
