import json


class Environment:
    def __init__(self, data=None):
        self._data = dict()
        if data:
            self._data.update(data)

    def __getattribute__(self, name):
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        else:
            return object.__getattribute__(self, "_data").get(name, "")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            object.__getattribute__(self, "_data")[name] = value

    def __getitem__(self, key):
        return object.__getattribute__(self, "_data").get(key, "")

    def __setitem__(self, key, value):
        object.__getattribute__(self, "_data")[key] = value

    def __str__(self):
        return str(json.dumps(self._data, indent=4, sort_keys=True))
