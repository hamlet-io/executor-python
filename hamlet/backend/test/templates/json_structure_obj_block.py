# NOTE: This file must remain valid python file in order to perform tests on it.
# NOTE: Imports can't be used inside a template block because all code will be merged into a single file.
# NOTE: The class is wrapped into function in order to make it testable. This adds an ability to provide parent classes
# at runtime, otherwise, the module will raise NameError


def JSONStructure(JSONValidator):
    class JSONStructure(JSONValidator):

        def __match(self, path, target):
            def validator():
                value = self._get_value_by_json_path(path)
                assert value == target, '{} doesn\'t match {}'.format(path, target)
            validator.__name__ = '{} == {}'.format(path, target)
            return validator

        def __len(self, path, target):
            def validator():
                value = self._get_value_by_json_path(path)
                assert len(value) == target, '{}.length={}!={}'.format(path, len(value), target)
            validator.__name__ = '{}.length == {}'.format(path, target)
            return validator

        def __exists(self, path):
            def validator():
                return self._get_value_by_json_path(path)
            validator.__name__ = '{} exists?'.format(path)
            return validator

        def __not_empty(self, path):
            def validator():
                value = self._get_value_by_json_path(path)
                assert_text = '{} is empty'.format(path)
                assert value is not None, assert_text
                if isinstance(value, (str, dict, list)):
                    assert len(value) > 0, assert_text
            validator.__name__ = 'not empty {}?'.format(path)
            return validator

        def match(self, path, target):
            self._validators.append(self.__match(path, target))
            return self

        def len(self, path, target):
            self._validators.append(self.__len(path, target))
            return self

        def exists(self, path):
            self._validators.append(self.__exists(path))
            return self

        def not_empty(self, path):
            self._validators.append(self.__not_empty(path))
            return self
    return JSONStructure
