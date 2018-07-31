import json


class PetroleumJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


class ToJSONMixin:
    def to_json(self):
        return json.dumps(self.__dict__,
                          cls=PetroleumJSONEncoder,
                          sort_keys=True)
