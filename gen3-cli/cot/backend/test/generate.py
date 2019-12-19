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
    append_file = False
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

        template_text = render(**casedata, name=casename)
        # if no output filename save to text output to be able to send it to stdout
        if output is None:
            text_output.append(template_text)
            continue

        # override file if it's the first case in the line
        # otherwise append generated tests
        mode = "wt+" if append_file else "wt"
        append_file = True
        with open(output, mode) as f:
            f.write(template_text)
    return "\n".join(text_output)
