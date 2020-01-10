class JSONValidator:
    def __init__(self, body):
        self._body = body
        self._validators = []

    @classmethod
    def from_file(cls, filename):
        try:
            with open(filename, "rt") as f:
                import json
                return cls(json.load(f))
        except FileNotFoundError as e:
            raise AssertionError("%s not found" % filename) from e
        except ValueError as e:
            raise AssertionError("%s is not a valid JSON" % filename) from e

    @staticmethod
    def _split_path(path):
        import re
        keys = []
        for m in re.finditer(r"(\w+)|\[(\d+)\]", path):
            key = m.group(1)
            index = m.group(2)
            if key is not None:
                keys.append(key)
            elif index is not None:
                keys.append(int(index))
        return keys

    @staticmethod
    def _format_keys_to_path(keys):
        result = ""
        for key in keys:
            if isinstance(key, int):
                result += "[%s]" % key
            else:
                result += ".%s" % key
        if result.startswith('.'):
            result = result[1:]
        return result

    def _get_value_by_json_path(self, path):
        keys = self._split_path(path)
        traversed_keys = []
        value = self._body
        for key in keys:
            traversed_keys.append(key)
            try:
                value = value[key]
            except (KeyError, IndexError) as e:
                raise AssertionError('{} does not exist'.format(self._format_keys_to_path(traversed_keys))) from e
        return value

    @property
    def errors(self):
        try:
            return self._errors
        except AttributeError:
            errors = []
            for validator in self._validators:
                try:
                    validator()
                except AssertionError as e:
                    msg = None
                    if e.args:
                        msg = e.args[0].split('\n')[0]
                    errors.append(
                        {
                            'rule': validator.__name__,
                            'msg': msg
                        }
                    )
            self._errors = errors
            return errors

    def assert_structure(self):
        import json
        if self.errors:
            raise AssertionError(json.dumps(self.errors, indent=4))
