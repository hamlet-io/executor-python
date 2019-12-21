class Structure:

    RESOURCES_KEY = 'Resources'
    RESOURCE_TYPE_KEY = 'Type'
    OUTPUT_KEY = 'Output'

    def __init__(self, body):
        self.__body = body
        self.__validators = []

    @staticmethod
    def __split_path(path):
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
    def __format_keys_to_path(keys):
        result = ""
        for key in keys:
            if isinstance(key, int):
                result += "[%s]" % key
            else:
                result += ".%s" % key
        if result.startswith('.'):
            result = result[1:]
        return result

    def __get_value_by_json_path(self, path):
        keys = self.__split_path(path)
        traversed_keys = []
        value = self.__body
        for key in keys:
            traversed_keys.append(key)
            try:
                value = value[key]
            except (KeyError, IndexError) as e:
                raise AssertionError('{} does not exist'.format(self.__format_keys_to_path(traversed_keys))) from e
        return value

    def __match(self, path, target):
        def validator():
            value = self.__get_value_by_json_path(path)
            assert value == target, '{} doesn\'t match {}'.format(path, target)
        validator.__name__ = '{} == {}'.format(path, target)
        return validator

    def __resource(self, id, type):
        def validator():
            resources = self.__body.get(self.RESOURCES_KEY, {})
            target = resources.get(id)
            assert target is not None, 'Resource {} is missing'.format(id)
            assert target[self.RESOURCE_TYPE_KEY] == type, 'resource {}.{}!={}'.format(
                id,
                self.RESOURCE_TYPE_KEY,
                type
            )
        validator.__name__ = 'resource {}.{} == {}'.format(id, self.RESOURCE_TYPE_KEY, type)
        return validator

    def __len(self, path, target):
        def validator():
            value = self.__get_value_by_json_path(path)
            assert len(value) == target, '{}.length[{}]!={}'.format(path, len(value), target)
        validator.__name__ = '{}.length == {}'.format(path, target)
        return validator

    def __exists(self, path):
        def validator():
            return self.__get_value_by_json_path(path)
        validator.__name__ = '{} exists?'.format(path)
        return validator

    def __not_empty(self, path):
        def validator():
            value = self.__get_value_by_json_path(path)
            assert_text = '{} is empty'.format(path)
            assert value is not None, assert_text
            if isinstance(value, (str, dict, list)):
                assert len(value) > 0, assert_text
        validator.__name__ = 'not empty {}?'.format(path)
        return validator

    def __output(self, id):
        def validator():
            output = self.__body.get(self.OUTPUT_KEY, {})
            value = output.get(id)
            assert value is not None, 'output {} is missing'.format(id)
        validator.__name__ = 'output {} exists'.format(id)
        return validator

    def match(self, path, target):
        self.__validators.append(self.__match(path, target))
        return self

    def resource(self, id, type):
        self.__validators.append(self.__resource(id, type))
        return self

    def output(self, id):
        self.__validators.append(self.__output(id))
        return self

    def len(self, path, target):
        self.__validators.append(self.__len(path, target))
        return self

    def exists(self, path):
        self.__validators.append(self.__exists(path))
        return self

    def not_empty(self, path):
        self.__validators.append(self.__not_empty(path))
        return self

    @property
    def errors(self):
        try:
            return self.__errors
        except AttributeError:
            errors = []
            for validator in self.__validators:
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
            self.__errors = errors
            return errors

    def assert_structure(self):
        import json
        if self.errors:
            raise AssertionError(json.dumps(self.errors, indent=4))


def structure_test(filename):
    try:
        with open(filename, "rt") as f:
            import json
            return Structure(json.load(f))
    except FileNotFoundError as e:
        raise AssertionError("%s not found" % filename) from e
    except ValueError as e:
        raise AssertionError("%s is not a valid JSON" % filename) from e
