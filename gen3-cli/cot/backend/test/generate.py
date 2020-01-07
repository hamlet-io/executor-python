import os
import json
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

    # merging casefiles
    cases = dict()
    for filename in filenames:
        if not filename.endswith(TESTCASE_EXT):
            raise ValueError('Invalid extension for [%s]. Must be [%s]' % (filename, TESTCASE_EXT))
        with open(filename, 'rt') as f:
            cases.update(**json.load(f))

    text = testcases_template.render(cases)
    if output is not None:
        with open(output, 'wt') as f:
            f.write(text)
        return ""
    return text
