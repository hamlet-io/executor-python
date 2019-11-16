import collections
import pytest
from cot.loggers import logging


logger = logging.getLogger('options')


def are_required_keys(keys):
    return keys.startswith('!')


def parse_keys(keys):
    # removing spaces and required flag
    return tuple(key.strip().strip('!') for key in keys.split(',') if key)


def get_key(keys, index):
    keys = parse_keys(keys)
    try:
        return keys[index]
    except IndexError:
        return keys[-1]


def is_values_collection(values):
    return isinstance(values, collections.abc.Iterable) and not isinstance(values, str)


def generate_incremental_required_options_collection(all_options):
    required_options = collections.OrderedDict()
    required_keys_max_parts = 1
    for keys, values in all_options.items():
        if are_required_keys(keys):
            if is_values_collection(values):
                value = values[0]
            else:
                value = values
            required_options[keys] = value
            required_keys_max_parts = max(required_keys_max_parts, len(parse_keys(keys)))

    if not required_options:
        logger.info(['no required options'])
        return

    for key_index in range(required_keys_max_parts):
        for max_arguments in range(len(required_options)):
            args = []
            str_args = []
            for keys, value in required_options.items():
                if len(str_args) >= max_arguments:
                    break
                key = get_key(keys, key_index)
                args.append(key)
                args.append(value)
                str_args.append(
                    '{} {}'.format(key, value)
                )
            logger.info('[required options: %s/%s]', len(str_args), len(required_options))
            logger.info(
                '\n'.join(str_args)
            )
            yield args


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
    Function does not create all posible combinations. Instead it freezes first value of all keys with
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
    def generate_args(key_index, fixed_value_keys=None, fixed_value_index=0, options=None):
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
                str_args.append('{} {}'.format(key, value))
        if fixed_value_index == 0:
            logger.info(
                '\n'.join(str_args)
            )
        else:
            logger.info(
                'Change:[%s %s]',
                get_key(fixed_value_keys, key_index),
                options[fixed_value_keys][fixed_value_index]
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
                            key_index,
                            fixed_value_keys,
                            fixed_value_index,
                            options
                        )
    # generating using only required options
    if len(required_options) != len(all_options):
        logger.info('[required]')
        if required_options:
            for args in generate_args_group(
                required_keys_max_parts,
                required_options,
                required_keys_collection_values
            ):
                yield args
        else:
            # command should run without options
            logger.info('None')
            yield []

    # generating using all options
    logger.info('[all]')
    for args in generate_args_group(
        all_keys_max_parts,
        all_options,
        optional_keys_collection_values
    ):
        yield args


def test_option_generation():
    options = collections.OrderedDict()
    options['!-a,--a'] = 'avalue'
    options['-b,--b'] = ['bvalue1', 'bvalue2']
    options['!-c,--c'] = ['cvalue1', 'cvalue2', 'cvalue3']
    options['-f,--f'] = [True, False]
    generator = generate_test_options_collection(options)
    # start with  only required options
    assert next(generator) == [
        '-a', 'avalue',
        '-c', 'cvalue1'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--c', 'cvalue1'
    ]
    # iteration over required collection values
    assert next(generator) == [
        '-a', 'avalue',
        '-c', 'cvalue2'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--c', 'cvalue2'
    ]
    assert next(generator) == [
        '-a', 'avalue',
        '-c', 'cvalue3'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--c', 'cvalue3'
    ]
    # then all options without required collection values
    assert next(generator) == [
        '-a', 'avalue',
        '-b', 'bvalue1',
        '-c', 'cvalue1',
        '-f'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--b', 'bvalue1',
        '--c', 'cvalue1',
        '--f'
    ]
    # collection values variations
    # iterating over '-b,--b' collection
    assert next(generator) == [
        '-a', 'avalue',
        '-b', 'bvalue2',
        '-c', 'cvalue1',
        '-f'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--b', 'bvalue2',
        '--c', 'cvalue1',
        '--f'
    ]
    # iterating over '-f,--f'
    assert next(generator) == [
        '-a', 'avalue',
        '-b', 'bvalue1',
        '-c', 'cvalue1',
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--b', 'bvalue1',
        '--c', 'cvalue1',
    ]
    with pytest.raises(StopIteration):
        next(generator)
