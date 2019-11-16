import collections
import pytest
from cot.loggers import logging


logger = logging.getLogger('OPTIONS GEN')


def generate_test_options_collection(options):
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
    max_keys_parts = 1
    collection_values_keys = []

    def parse_keys(keys):
        return tuple(key.strip() for key in keys.split(',') if key)

    def get_key(keys, index):
        keys = parse_keys(keys)
        try:
            return keys[index]
        except IndexError:
            return keys[-1]

    def is_values_collection(values):
        return isinstance(values, collections.abc.Iterable) and not isinstance(values, str)

    for keys in options:
        max_keys_parts = max(max_keys_parts, len(parse_keys(keys)))

    for keys, values in options.items():
        if is_values_collection(values):
            collection_values_keys.append(keys)

    # fixed_value_keys is plural because it's a commaseparated list of keys
    def generate_args(key_index, fixed_value_keys=None, fixed_value_index=0):
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

    for key_index in range(max_keys_parts):
        yield generate_args(key_index)
    # starting from index 1 because previous generation conains all 0 indexes
    if collection_values_keys:
        for fixed_value_keys in collection_values_keys:
            # logger.info('Fixed keys:%s', fixed_value_keys)
            for fixed_value_index in range(1, len(options[fixed_value_keys])):
                for key_index in range(max_keys_parts):
                    yield generate_args(key_index, fixed_value_keys, fixed_value_index)


def test_option_generation():
    options = collections.OrderedDict()
    options['-a,--a'] = 'avalue'
    options['-b,--b'] = ['bvalue1', 'bvalue2']
    options['-c,--c'] = ['cvalue1', 'cvalue2', 'cvalue3']
    options['-f,--f'] = [True, False]
    generator = generate_test_options_collection(options)
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
    # iterating over '-c,--c' collection
    assert next(generator) == [
        '-a', 'avalue',
        '-b', 'bvalue1',
        '-c', 'cvalue2',
        '-f'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--b', 'bvalue1',
        '--c', 'cvalue2',
        '--f'
    ]
    assert next(generator) == [
        '-a', 'avalue',
        '-b', 'bvalue1',
        '-c', 'cvalue3',
        '-f'
    ]
    assert next(generator) == [
        '--a', 'avalue',
        '--b', 'bvalue1',
        '--c', 'cvalue3',
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
