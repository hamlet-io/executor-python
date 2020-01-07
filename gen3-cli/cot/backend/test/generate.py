import os
import json
from cot.backend.common.exceptions import UserFriendlyBackendException
from .renderer import testcases_template


TESTCASE_EXT = '-testcase.json'


def run(
    filenames=None,
    output=None,
    directory=None
):
    filenames = filenames or []
    # searching testcase files in given directory if no files provided
    if not filenames and directory:
        for name in os.listdir(directory):
            if name.endswith(TESTCASE_EXT):
                filenames.append(os.path.join(directory, name))
    # if after all no files found raise an error
    if not filenames:
        raise UserFriendlyBackendException("No testcase files found!")
    # merging casefiles
    cases = dict()
    for filename in filenames:
        if not filename.endswith(TESTCASE_EXT):
            raise UserFriendlyBackendException(f'Invalid extension for {filename}. Must be {TESTCASE_EXT}')
        with open(filename, 'rt') as f:
            # TODO: add testcase data schema check
            cases.update(**json.load(f))

    # if files have no testcases data
    if not cases:
        raise UserFriendlyBackendException("No testcases found!")

    text = testcases_template.render(cases)
    if output is not None:
        with open(output, 'wt') as f:
            f.write(text)
        return ""
    return text
