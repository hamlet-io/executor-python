import os
import tempfile
from cot.backend.test.generate import run as generate_test_backend
from .conftest import DATA_DIR


def test():
    with tempfile.TemporaryDirectory() as dir:
        output_filename = os.path.join(dir, 'test.py')
        casefilename = os.path.join(DATA_DIR, 'generate-cf-test-template.json')
        generate_test_backend([casefilename], output_filename)
        print(generate_test_backend([casefilename], None))
