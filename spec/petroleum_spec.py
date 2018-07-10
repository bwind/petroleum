from expects import expect, raise_error
from mamba import description, it
from petroleum import Task


with description('task'):
    with it('can instantiate Task'):
        expect(lambda: Task(name='test')).not_to(raise_error(Exception))
