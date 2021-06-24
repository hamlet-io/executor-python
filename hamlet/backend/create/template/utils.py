import re
from hamlet.loggers import logging


logger = logging.getLogger('UTILS')


def deep_dict_update(a, b):
    for b_key, b_value in b.items():
        a_value = a.get(b_key)
        if isinstance(a_value, dict) and isinstance(b_value, dict):
            deep_dict_update(a_value, b_value)
        else:
            a[b_key] = b_value


# -- semver handling --
# Comparisons/naming roughly aligned to https://github.com/npm/node-semver
# in case we want to replace these routines with calls to this package via
# docker
def semver_valid(version):
    pattern = r'^v?(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(\-([^+]+))?(\+(.*))?$'
    match = re.search(pattern, version)
    if not match:
        raise ValueError(f'Invalid semantic version format "{version}"')
    major = match.group(1)
    minor = match.group(2)
    patch = match.group(3)
    prere = match.group(5)
    build = match.group(7)
    return (major, minor, patch, prere, build,)


# Strip any leading "v" (note we handle leading = in semver_satisfies)
# Convert any range indicators ("x" or "X") to 0
# * not supported as substitute for x
def semver_clean(version):
    # Handle the full format
    pattern = r'^v?(0|[1-9][0-9]*|x|X)\.(0|[1-9][0-9]*|x|X)\.(0|[1-9][0-9]*|x|X)(\-([^+]+))?(\+(.*))?$'
    match = re.search(pattern, version)
    if match:
        major = match.group(1).lower().replace('x', '0')
        minor = match.group(2).lower().replace('x', '0')
        patch = match.group(3).lower().replace('x', '0')
        prere = match.group(5)
        build = match.group(7)
        version = f'{major}.{minor}.{patch}'
        version = f'{version}-{prere}' if prere else version
        version = f'{version}+{build}' if build else version
        return version
    # Handle major.minor
    pattern = r'^v?(0|[1-9][0-9]*|x|X)\.(0|[1-9][0-9]*|x|X)$'
    match = re.search(pattern, version)
    if match:
        major = match.group(1).lower().replace('x', '0')
        minor = match.group(2).lower().replace('x', '0')
        return f'{major}.{minor}.0'
    # Handle major
    pattern = r'^v?(0|[1-9][0-9]*|x|X)$'
    match = re.search(pattern, version)
    if match:
        major = match.group(1).lower().replace('x', '0')
        return f'{major}.0.0'
    raise ValueError(f'Invalid semantic version format "{version}"')


def semver_compare(v1, v2):

    v1 = semver_clean(v1)
    v2 = semver_clean(v2)

    v1_components = semver_valid(v1)
    v2_components = semver_valid(v2)

    # MAJOR, MINOR and PATCH should compare numericaly
    for i in range(3):
        if v1_components[i] > v2_components[i]:
            return 1
        elif v1_components[i] < v2_components[i]:
            return -1

    # PREREL, BUILD should compare with the ASCII order.
    for i in range(3, 5):
        if not v1_components[i] and not v2_components[i]:
            continue
        if not v1_components[i] and v2_components[i]:
            return -1
        if v1_components[i] and not v2_components[i]:
            return 1
        if v1_components[i] < v2_components[i]:
            return -1
        else:
            return 1
    return 0


# a comparator set is a list of comparators, true if all comparators are true
# a comparator is an operator and a version
def semver_satisfies(version, comparators_set):
    for comparator in comparators_set:
        logger.debug('Checking comparator "%s" ...', comparator)
        match = re.match(r'^(<=|>=|=|<|>)(.+)$', comparator)
        if not match:
            raise ValueError(f'Unknown comparator {comparator}')
        operator = match.group(1)
        comparator_version = semver_clean(match.group(2))
        comparator_result = semver_compare(version, comparator_version)
        if operator == '<' and comparator_result < 0:
            continue
        elif operator == '>' and comparator_result > 0:
            continue
        elif operator == '=' and comparator_result == 0:
            continue
        elif operator == '<=' and comparator_result <= 0:
            continue
        elif operator == '>=' and comparator_result >= 0:
            continue
        else:
            return False
    return True


def semver_upgrade_list(upgrade_list, maximum_version):
    # assuming the list is ordered
    for i in range(len(upgrade_list)):
        if semver_compare(maximum_version, upgrade_list[i]) < 0:
            return upgrade_list[:i]
    return upgrade_list
