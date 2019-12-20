import os
import tempfile
from cot.backend.test.generate import run as generate_test_backend
from .conftest import DATA_DIR


def test():
    with tempfile.TemporaryDirectory() as dir:
        # testing single file with output file option and without
        output_filename = os.path.join(dir, 'test.py')
        casefilename = os.path.join(DATA_DIR, 'testcase', 'secure.json')
        generate_test_backend([casefilename], output_filename)
        with open(output_filename, 'rt') as f:
            file_text = f.read()
        stdout_text = generate_test_backend([casefilename], None)
        assert file_text == stdout_text
        assert "test_secure():" in file_text
        casefiles = [
            'secure.json',
            'insecure.json',
            'structure-good.json',
            'structure-bad.json',
            'invalid-syntax.json',
            'valid-syntax.json'
        ]
        # testing multiple files with output file option and without
        casefiles = list(map(lambda n: os.path.join(DATA_DIR, 'testcase', n), casefiles))
        generate_test_backend(casefiles, output_filename)
        with open(output_filename, 'rt') as f:
            file_text = f.read()
        stdout_text = generate_test_backend(casefiles, None)
        assert file_text == stdout_text
        assert "test_secure():" in file_text
        assert "test_insecure():" in file_text
        assert "test_structureGood():" in file_text
        assert "test_structureBad():" in file_text
        assert "test_validSyntax():" in file_text
        assert "test_invalidSyntax():" in file_text
