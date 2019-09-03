from dataclasses import dataclass

from petroleum.json_encoder import ToJSONMixin


@dataclass
class ConditionalTask(ToJSONMixin):
    task: object
    condition: object
    default: bool = False
