import os
import json
from marshmallow import ValidationError
from hamlet.backend.common.exceptions import BackendException
from .renderer import testcases_template
from .testcase_schema import Testcase as TestcaseSchema


TESTCASE_EXT = "-testcase.json"


def run(filenames=None, output=None, directory=None):
    filenames = filenames or []
    # searching testcase files in given directory if no files provided
    if not filenames and directory:
        for name in os.listdir(directory):
            if name.endswith(TESTCASE_EXT):
                filenames.append(os.path.join(directory, name))
    # if after all no files found raise an error
    if not filenames:
        raise BackendException("No testcase files found!")
    # merging casefiles
    cases = dict()
    for filename in filenames:
        if not filename.endswith(TESTCASE_EXT):
            raise BackendException(
                f"Invalid extension for {filename}. Must be {TESTCASE_EXT}"
            )
        with open(filename, "rt") as f:
            testcase_file_data = json.load(f)
            for name, testcase in testcase_file_data.items():
                try:
                    TestcaseSchema().load(testcase)
                except ValidationError as e:
                    message = json.dumps(e.messages, indent=4)
                    raise BackendException(
                        f'Invalid testcase schema in {filename}, testcase "{name}". \n\nErrors: \n{message}'
                    ) from e
            cases.update(**testcase_file_data)

    # if files have no testcases data
    if not cases:
        raise BackendException("No testcases found!")

    text = testcases_template.render(cases)
    if output is not None:
        with open(output, "wt") as f:
            f.write(text)
        return ""
    return text
