"""
This module's idea is the automation of very repetitive tests which we must have
to test the correctness of our cli configuration. This module's functions greatly reduce the number of lines
that we need to maintain. And because of that tests become much more accurate
and reliable.

Sure, manual individual testing is somewhat better but I think that we'll test "backend" part of our script separately.
Therefore this module will be useful even after we'll rewrite everything in python.
"""


import copy
import collections
from unittest import mock
import pytest
import click
from click.testing import CliRunner
from hamlet.loggers import logging


logger = logging.getLogger("options")


def are_required_keys(keys):
    return keys.startswith("!")


def parse_keys(keys):
    # removing spaces and required flag
    return tuple(key.strip().strip("!") for key in keys.split(",") if key)


def get_key(keys, index):
    keys = parse_keys(keys)
    try:
        return keys[index]
    except IndexError:
        return keys[-1]


def is_values_collection(values):
    return isinstance(values, collections.abc.Iterable) and not isinstance(values, str)


def generate_incremental_required_options_collection(all_options):
    """
    Generates collection of cli required option(marked by!)
    Used to test that command can't run without all being given all required options.
    For example we have 3 required options with an alternative key each.
    Function will produce generator which will give:
    ([], True),
    (
        [
            -first-required-option, value
        ],
        True
    ),
    (
        [
            -first-required-option, value,
            -second-required-option, value
        ],
        True
    ),
    (
        [
            -first-required-option, value,
            -second-required-option, value
            -third-required-option, value
        ],
        False
    )
    Where first element of tuple is args list and second element is bool error flag.
    Error flag used to select correct check for given args list.
    """
    required_options = collections.OrderedDict()
    required_keys_max_parts = 1
    for keys, values in all_options.items():
        if are_required_keys(keys):
            if is_values_collection(values):
                value = values[0]
            else:
                value = values
            required_options[keys] = value
            required_keys_max_parts = max(
                required_keys_max_parts, len(parse_keys(keys))
            )

    if not required_options:
        logger.info(["no required options"])
        return

    for key_index in range(required_keys_max_parts):
        for max_arguments in range(len(required_options) + 1):
            args = []
            str_args = []
            for keys, value in required_options.items():
                if len(str_args) >= max_arguments:
                    break
                key = get_key(keys, key_index)
                args.append(key)
                args.append(value)
                str_args.append("{} {}".format(key, value))
            logger.info(
                "[required options: %s/%s]", len(str_args), len(required_options)
            )
            logger.info("\n".join(str_args))
            yield args, len(str_args) < len(required_options)


def generate_test_options_collection(all_options):
    """
    Generates collection of CLI options based on OrderedDict with next structure:
        ordered_dict['-o, --option'] = 'value'
        ordered_dict['-m', '--multi'] = ['a', 'b']
    Results:
        [
            '-o', 'value',
            '-m', 'a'
        ],
        [
            '--option', 'value',
            '--multi', 'a'
        ],
        [
            '-o', 'value',
            '-m', 'b'
        ],
        [
            '--option', 'value',
            '--multi', 'b'
        ]
    Function does not create all possible combinations. Instead it freezes first value of all keys with
    iterable collection values and then creates variations by iterating over one of the keys with collection values
    untill all of them iterated.
    """
    required_options = collections.OrderedDict()
    all_keys_max_parts = 1
    required_keys_max_parts = 1
    required_keys_collection_values = []
    optional_keys_collection_values = []

    for keys, values in all_options.items():
        key_parts = parse_keys(keys)
        all_keys_max_parts = max(all_keys_max_parts, len(key_parts))
        required = are_required_keys(keys)
        if required:
            required_options[keys] = values
            required_keys_max_parts = max(required_keys_max_parts, len(key_parts))
        if is_values_collection(values):
            if required:
                required_keys_collection_values.append(keys)
            else:
                optional_keys_collection_values.append(keys)

    # fixed_value_keys is plural because it's a commaseparated list of keys
    def generate_args(
        key_index, fixed_value_keys=None, fixed_value_index=0, options=None
    ):
        args = []
        str_args = []
        for keys, values in options.items():
            key = get_key(keys, key_index)
            if is_values_collection(values):
                if keys == fixed_value_keys:
                    value = values[fixed_value_index]
                else:
                    value = values[0]
            else:
                value = values
            if isinstance(value, bool):
                if value:
                    args.append(key)
                    str_args.append(key)
            else:
                args.append(key)
                args.append(value)
                str_args.append("{} {}".format(key, value))
        if fixed_value_index == 0:
            logger.info("\n".join(str_args))
        else:
            logger.info(
                "Change:[%s %s]",
                get_key(fixed_value_keys, key_index),
                options[fixed_value_keys][fixed_value_index],
            )
        return args

    def generate_args_group(max_keys_parts, options, collection_values_keys):
        for key_index in range(max_keys_parts):
            yield generate_args(key_index, options=options)
        # starting from index 1 because previous generation conains all 0 indexes
        if collection_values_keys:
            for fixed_value_keys in collection_values_keys:
                for fixed_value_index in range(1, len(options[fixed_value_keys])):
                    for key_index in range(max_keys_parts):
                        yield generate_args(
                            key_index, fixed_value_keys, fixed_value_index, options
                        )

    # generating using only required options
    if len(required_options) != len(all_options):
        logger.info("[required]")
        if required_options:
            for args in generate_args_group(
                required_keys_max_parts,
                required_options,
                required_keys_collection_values,
            ):
                yield args
        else:
            # command should run without options
            logger.info("None")
            yield []

    # generating using all options
    logger.info("[all]")
    for args in generate_args_group(
        all_keys_max_parts, all_options, optional_keys_collection_values
    ):
        yield args


# pure utility function
def options_dict_to_list(options):
    args = []
    for key, value in options.items():
        args.append(key)
        args.append(value)
    return args


def run_single_validatable_option_test(
    runner,
    cmd,
    runner_mock,
    options,
    key,
    incorrect,
    correct,
):
    """
    Test option validation rule by providing incorrect and correct values for the same option.
    That's is not the best test in the world, but click env is quite isolated.
    Therefore I can't capture click's standard exceptions.
    """
    logger.info("[validation test:%s]", key)
    logger.info("invalid value:%s", incorrect)
    options = copy.deepcopy(options)
    options[key] = incorrect
    result = runner.invoke(cmd, options_dict_to_list(options))
    assert result.exit_code == 2, result.output
    assert runner_mock.call_count == 0
    logger.info("valid value:%s", correct)
    options[key] = correct
    result = runner.invoke(cmd, options_dict_to_list(options))
    assert result.exit_code == 0, result.output
    assert runner_mock.call_count == 1
    runner_mock.call_count = 0
    logger.info("[success]")


def run_validatable_option_test(runner, cmd, runner_mock, options, tests):
    """
    Handy shortcut for testing multiply options of the same command using run_single_validatable_option_test
    """
    for key, incorrect, correct in tests:
        run_single_validatable_option_test(
            runner, cmd, runner_mock, options, key, incorrect, correct
        )


def run_options_test(runner, cmd, options, runner_mock):
    """
    Shortcut which runs generalized tests:
    1. Testing that no more options exist
    2. Testing that required options are required.
    3. Testing that all options accepted and all expected values pass validation.
    """
    assert len(cmd.params) == len(options)
    for args, error in generate_incremental_required_options_collection(options):
        result = runner.invoke(cmd, args)
        if error:
            assert result.exit_code == 2, result.output
            assert runner_mock.call_count == 0
        else:
            logger.info(result.exception)
            assert result.exit_code == 0, result.output
            assert runner_mock.call_count == 1
            runner_mock.call_count = 0

    for args in generate_test_options_collection(options):
        result = runner.invoke(cmd, args)
        logger.info(result.exc_info)
        print(result.stdout)
        assert result.exit_code == 0, result.output
        assert runner_mock.call_count == 1
        runner_mock.call_count = 0


def test_run_options_test():
    runner_mock = mock.MagicMock()
    runner = CliRunner()

    @click.command()
    @click.option("-a", "--a", required=True)
    @click.option("-b", "--b", required=True, type=click.Choice(["bvalue1", "bvalue2"]))
    @click.option("-c", "--c", type=click.Choice(["cvalue1", "cvalue2", "cvalue3"]))
    @click.option("-f", "--f", is_flag=True)
    def test_command(a, b, c, f):
        runner_mock()

    def run_test(options, error=True):
        if error:
            with pytest.raises(AssertionError):
                run_options_test(runner, test_command, options, runner_mock)
        else:
            run_options_test(runner, test_command, options, runner_mock)

    correct_options = collections.OrderedDict()
    correct_options["!-a,--a"] = "avalue"
    correct_options["!-b,--b"] = ["bvalue1", "bvalue2"]
    correct_options["-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]
    correct_options["-f,--f"] = [True, False]

    # tests should pass for correct options
    run_test(correct_options, False)

    not_all_options = collections.OrderedDict()
    not_all_options["!-a,--a"] = "avalue"
    not_all_options["!-b,--b"] = ["bvalue1", "bvalue2"]
    not_all_options["-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]

    # should fail because not all options listed
    run_test(not_all_options)

    incorrect_value_options = collections.OrderedDict()
    incorrect_value_options["!-a,--a"] = "avalue"
    incorrect_value_options["!-b,--b"] = ["bvalue1", "bvalue2", "bvalue3"]
    incorrect_value_options["-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]
    incorrect_value_options["-f,--f"] = [True, False]

    # should fail because bvalue3 is not accepted
    run_test(incorrect_value_options)

    required_is_optional_options = collections.OrderedDict()
    required_is_optional_options["!-a,--a"] = "avalue"
    required_is_optional_options["-b,--b"] = ["bvalue1", "bvalue2"]
    required_is_optional_options["-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]
    required_is_optional_options["-f,--f"] = [True, False]

    # should fail because b is not required
    run_test(required_is_optional_options)

    optional_is_required_options = collections.OrderedDict()
    optional_is_required_options["!-a,--a"] = "avalue"
    optional_is_required_options["!-b,--b"] = ["bvalue1", "bvalue2"]
    optional_is_required_options["!-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]
    optional_is_required_options["-f,--f"] = [True, False]

    # should fail because c is required
    run_test(optional_is_required_options)


def test_validatable_options_test():
    runner_mock = mock.MagicMock()
    runner = CliRunner()

    @click.command()
    @click.option("-r", required=True, type=click.INT)
    @click.option("-o", type=click.INT)
    def test_command(r, o):
        runner_mock()

    def run_test(options, error=True):
        def start():
            run_validatable_option_test(
                runner, test_command, runner_mock, {"-r": "10"}, options
            )

        if error:
            with pytest.raises(AssertionError):
                start()
        else:
            start()

        # will raise error because all values valid
        run_test([("-r", "10", "10"), ("-o", "not_an_int", "10")])
        # will raise error because -r option incorrect value passes validation
        run_test([("-r", "10", "not_an_int"), ("-o", "not_an_int", "10")])
        # will raise error because -o option all invalid
        run_test([("-r", "not_an_int", "10"), ("-o", "not_an_int", "not_an_int")])
        # tests must pass
        run_test([("-r", "not_an_int", "10"), ("-o", "not_an_int", "10")], False)


def test_generate_incremental_required_options_collection():
    options = collections.OrderedDict()
    options["!-a,--a"] = "avalue"
    options["-b,--b"] = ["bvalue1", "bvalue2"]
    options["!-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]
    options["-f,--f"] = [True, False]

    generator = generate_incremental_required_options_collection(options)
    assert next(generator) == ([], True)
    assert next(generator) == (["-a", "avalue"], True)
    assert next(generator) == (["-a", "avalue", "-c", "cvalue1"], False)
    assert next(generator) == ([], True)
    assert next(generator) == (["--a", "avalue"], True)
    assert next(generator) == (["--a", "avalue", "--c", "cvalue1"], False)
    with pytest.raises(StopIteration):
        next(generator)


def test_option_generation():
    options = collections.OrderedDict()
    options["!-a,--a"] = "avalue"
    options["-b,--b"] = ["bvalue1", "bvalue2"]
    options["!-c,--c"] = ["cvalue1", "cvalue2", "cvalue3"]
    options["-f,--f"] = [True, False]
    generator = generate_test_options_collection(options)
    # start with  only required options
    assert next(generator) == ["-a", "avalue", "-c", "cvalue1"]
    assert next(generator) == ["--a", "avalue", "--c", "cvalue1"]
    # iteration over required collection values
    assert next(generator) == ["-a", "avalue", "-c", "cvalue2"]
    assert next(generator) == ["--a", "avalue", "--c", "cvalue2"]
    assert next(generator) == ["-a", "avalue", "-c", "cvalue3"]
    assert next(generator) == ["--a", "avalue", "--c", "cvalue3"]
    # then all options without required collection values
    assert next(generator) == ["-a", "avalue", "-b", "bvalue1", "-c", "cvalue1", "-f"]
    assert next(generator) == [
        "--a",
        "avalue",
        "--b",
        "bvalue1",
        "--c",
        "cvalue1",
        "--f",
    ]
    # collection values variations
    # iterating over '-b,--b' collection
    assert next(generator) == ["-a", "avalue", "-b", "bvalue2", "-c", "cvalue1", "-f"]
    assert next(generator) == [
        "--a",
        "avalue",
        "--b",
        "bvalue2",
        "--c",
        "cvalue1",
        "--f",
    ]
    # iterating over '-f,--f'
    assert next(generator) == [
        "-a",
        "avalue",
        "-b",
        "bvalue1",
        "-c",
        "cvalue1",
    ]
    assert next(generator) == [
        "--a",
        "avalue",
        "--b",
        "bvalue1",
        "--c",
        "cvalue1",
    ]
    with pytest.raises(StopIteration):
        next(generator)
