import os
import json
from .renderer import cf_test_template


TESTCASE_EXT = '.testcase.json'


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

    text_output = []
    # merging casefiles
    cases = dict()
    for filename in filenames:
        if not filename.endswith(TESTCASE_EXT):
            raise ValueError('Invalid extension for [%s]. Must be [%s]' % (filename, TESTCASE_EXT))
        with open(filename, 'rt') as f:
            cases.update(**json.load(f))
    # to make idempotent testcases ordering
    casenames = list(cases.keys())
    casenames.sort()
    for casename in casenames:

        casedata = cases[casename]
        filename, ext = os.path.splitext(casedata['filename'])
        render = None
        # selecting proper renderer based on tested filename extension
        # could be changed in the future for more direct type indication
        if ext == '.json':
            render = cf_test_template.render

        # if we can't find proper renderer skip the case
        # maybe throw error, still thinking what will be better
        if render is None:
            continue

        text_output.append(render(**casedata, name=casename))

    # preparing text to ensure equiality between file and text output
    text = "\n\n".join(text_output)
    if output is not None:
        with open(output, 'wt') as f:
            f.write(text)
        return ""
    return text
