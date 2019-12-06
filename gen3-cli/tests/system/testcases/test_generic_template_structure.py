# from cot.loggers import root


class Template:

    RESOURCES_KEY = 'Resources'
    RESOURCE_TYPE_KEY = 'Type'
    OUTPUT_KEY = 'Output'

    def __init__(self, body):
        self.__body = body
        self.__validators = []

    def __get_value_by_json_path(self, path):
        keys = path.split('.')
        traversed_path = []
        value = self.__body
        for key in keys:
            traversed_path.append(key)
            try:
                try:
                    if isinstance(value, list):
                        key = int(key)
                except ValueError as e:
                    raise KeyError() from e
                value = value[key]
            except KeyError:
                raise AssertionError('{} does not exist'.format('.'.join(traversed_path)))
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


def test():
    body = {
        'path': {
            'exists': []
        },
        'not': {
            'empty': {
                'list': [1, 2],
                'scalar': 1,
                'obj': {
                    '1': 'value',
                    '2': 'value',
                    '3': 'value'
                }
            }
        },
        'empty': {
            'list': [],
            'scalar': None,
            'obj': {}
        },
        Template.RESOURCES_KEY: {
            'TestResource': {
                Template.RESOURCE_TYPE_KEY: 'TestType'
            }
        },
        Template.OUTPUT_KEY: {
            'TestOutput': {
                'Value': 'value'
            }
        }
    }
    template = Template(body)

    template.match('path.exists', [])

    template.resource('TestResource', 'TestType')

    template.output('TestOutput')

    template.len('not.empty.list', 2)
    template.len('not.empty.obj', 3)

    template.exists('path.exists')

    template.not_empty('not.empty.list')
    template.not_empty('not.empty.scalar')
    template.not_empty('not.empty.obj')
    assert not template.errors

    template = Template(body)
    template.match('path.exists', [1])
    template.match('not.empty.scalar', 10)
    template.match('not.empty.obj', {'1': 'value'})
    assert len(template.errors) == 3

    template = Template(body)
    template.resource('NotExists', 'TestType')
    template.resource('TestResource', 'WrongType')
    assert len(template.errors) == 2

    template = Template(body)
    template.output('NotExists')
    assert len(template.errors) == 1

    template = Template(body)
    template.len('not.empty.list', 3)
    template.len('not.empty.obj', 2)
    assert len(template.errors) == 2

    template = Template(body)
    template.exists('not.path.exists')
    assert len(template.errors) == 1

    template = Template(body)
    template.not_empty('empty.list')
    template.not_empty('empty.scalar')
    template.not_empty('empty.obj')
    assert len(template.errors) == 3
