from hamlet.loggers import logging
from hamlet.utils import DynamicOption

# TEST_OPTIONS = collections.OrderedDict()
# TEST_OPTIONS['!-i,--id,id'] = ('id')
# TEST_OPTIONS['--name,name'] = ('name', 'id')
# TEST_OPTIONS['--param,param'] = ('non-default', 'default')

logger = logging.getLogger("test-generate")


def __inputlines(*args):
    return "\n".join(list(str(a) for a in args))


def __split_key(key):
    key = key.strip("! ")
    parts = tuple(part.strip() for part in key.split(",") if part.strip())
    if len(parts) < 2:
        raise ValueError('Key should be in format:"--option-key, param_name"')
    return parts


def __get_key_part(key, index):
    parts = __split_key(key)
    return parts[max(len(parts) - 2, index)]


def __get_param_name_from_key(key):
    return __split_key(key)[-1]


def __is_required_key(key):
    return key.strip().startswith("!")


def __get_value(values):
    if isinstance(values, (list, tuple)):
        return values[0]
    else:
        return values


def __get_default(values):
    if isinstance(values, (list, tuple)):
        return values[1]
    raise ValueError("default value not set")


def __generate_prompt_options_testcase(template):
    for required_only in [True, False]:
        options = []
        options_str = []
        input = []
        expected = {}
        for keys, values in template.items():
            required = __is_required_key(keys)
            param = __get_param_name_from_key(keys)
            value = __get_value(values)
            if not required_only or required:
                if isinstance(value, bool):
                    input.append("y" if value else "n")
                else:
                    input.append(str(value))
            expected[param] = (
                value if not required_only or required else __get_default(values)
            )
        yield {
            "options": options,
            "options_str": options_str,
            "input": __inputlines(*input, "y"),
            "expected": expected,
        }


def __generate_options_testcase(template):
    for required_only in [True, False]:
        max_key_parts = 1
        for key in template:
            key_parts = __split_key(key)
            max_key_parts = max(max_key_parts, len(key_parts) - 1)
        for key_index in range(max_key_parts):
            options = []
            options_str = []
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
                            options_str.append(key)
                    else:
                        options_str.append("{} {}".format(key, value))
                        options.append(key)
                        options.append(value)
                expected[param] = (
                    value if not required_only or required else __get_default(values)
                )
            yield {
                "options": options,
                "options_str": options_str,
                "input": None,
                "expected": expected,
            }


def __generate_testcases(options):
    for case in __generate_options_testcase(options):
        yield case
    for case in __generate_prompt_options_testcase(options):
        yield case


def __log_testcase(testcase, cmd):
    output = "\n"
    output += "Options:\n"
    for option in testcase["options_str"]:
        output += "  {}\n".format(option)
    if testcase["input"]:
        output += "Input:\n"
        for input in testcase["input"].split("\n"):
            output += "  {}\n".format(input)
    output += "Expected:\n"
    for key, value in testcase["expected"].items():
        if isinstance(value, str) and not value:
            value = '""'
        output += "  {}={}\n".format(key, value)
    logger.info(output)


def run_generate_command_test(runner, cmd, cmd_backend_run, options):
    # check missing options
    dynamic_params = [p.name for p in cmd.params if isinstance(p, DynamicOption)]
    options_params = [__get_param_name_from_key(key) for key in options]
    missing = []
    for name in dynamic_params:
        if name not in options_params:
            missing.append(name)
    assert not missing

    # 4 testcases
    # only required options
    # all options
    # only required prompt
    # all prompt
    for case in __generate_testcases(options):
        cmd_backend_run.reset_mock()
        __log_testcase(case, cmd)
        result = runner.invoke(cmd, case["options"], input=case["input"])
        assert result.exit_code == 0, result.output
        cmd_backend_run.assert_called_once()
        cmd_backend_run.call_args_list[0].kwargs == case["expected"]
    cmd_backend_run.reset_mock()
