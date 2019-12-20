import os
import json
from .renderer import cf_test_template


def run(
    filenames=None,
    output=None
):
    text_output = []
    # merging casefiles
    cases = dict()
    for filename in filenames:
        with open(filename, 'rt') as f:
            cases.update(**json.load(f))
    for casename in cases:

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

    text = "\n\n".join(text_output)
    if output is not None:
        with open(output, 'wt') as f:
            f.write(text)
        return ""
    return text
