from petroleum import PetroleumObject
from petroleum.json_encoder import ToJSONMixin


class ConditionalTask(PetroleumObject, ToJSONMixin):
    def __init__(self, task, condition, default=False):
        self.task = task
        self.condition = condition
        self.default = default
