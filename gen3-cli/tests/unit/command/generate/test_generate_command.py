from cot.loggers import logging
# TEST_OPTIONS = collections.OrderedDict()
# TEST_OPTIONS['!-i,--id,id'] = ('id')
# TEST_OPTIONS['--name,name'] = ('name', 'id')
# TEST_OPTIONS['--param,param'] = ('non-default', 'default')

logger = logging.getLogger('CMD_TEST')


def __inputlines(*args):
    return "\n".join(list(str(a) for a in args))


def __split_key(key):
    key = key.strip('! ')
    parts = tuple(part.strip() for part in key.split(',') if part.strip())
    if len(parts) < 2:
        raise ValueError('Key should be in format:"--option-key, param_name"')
    return parts


def __get_key_part(key, index):
    parts = __split_key(key)
    return parts[max(len(parts)-2, index)]


def __get_param_name_from_key(key):
    return __split_key(key)[-1]


def __is_required_key(key):
    return key.strip().startswith('!')


def __get_value(values):
    if isinstance(values, (list, tuple)):
        return values[0]
    else:
        return values


def __get_default(values):
    if isinstance(values, (list, tuple)):
        return values[1]
    raise ValueError('default value not set')


def __generate_prompt_options_testcase(template):
    for required_only in [True, False]:
        options = ['--prompt']
        if required_only:
            options.append('--use-default')
        input = []
        expected = {}
        for keys, values in template.items():
            required = __is_required_key(keys)
            param = __get_param_name_from_key(keys)
            value = __get_value(values)
            if not required_only or required:
                if isinstance(value, bool):
                    input.append('y' if value else 'n')
                else:
                    input.append(str(value))
            expected[param] = value if not required_only or required else __get_default(values)
        yield {
            'options': options,
            'input': __inputlines(*input, 'y'),
            'expected': expected
        }


def __generate_options_testcase(template):
    for required_only in [True, False]:
        max_key_parts = 1
        for key in template:
            key_parts = __split_key(key)
            max_key_parts = max(max_key_parts, len(key_parts)-1)
        for key_index in range(max_key_parts):
            options = []
            expected = {}
            for keys, values in template.items():
                key = __get_key_part(keys, key_index)
                value = __get_value(values)
                required = __is_required_key(keys)
                param = __get_param_name_from_key(keys)
                if not required_only or required:
                    if isinstance(value, bool):
                        if value:
                            options.append(key)
                    else:
                        options.append(key)
                        options.append(value)
                expected[param] = value if not required_only or required else __get_default(values)
            yield {
                'options': options,
                'input': None,
                'expected': expected
            }


def __generate_testcases(options):
    for case in __generate_options_testcase(options):
        yield case
    for case in __generate_prompt_options_testcase(options):
        yield case


def run_generate_command_test(runner, cmd, cmd_backend_run, options):
    import json
    for case in __generate_testcases(options):
        cmd_backend_run.reset_mock()
        logger.info('\n%s', json.dumps(case, indent=4))
        result = runner.invoke(
            cmd,
            case['options'],
            input=case['input']
        )
        assert result.exit_code == 0, result.output
        cmd_backend_run.assert_called_once()
        cmd_backend_run.call_args_list[0].kwargs == case['expected']
    cmd_backend_run.reset_mock()
