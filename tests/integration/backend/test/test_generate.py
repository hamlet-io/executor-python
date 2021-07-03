import os
import json
import shutil
import tempfile
import pytest
from hamlet.backend.common.exceptions import BackendException
from hamlet.backend.test.generate import run as generate_test_backend
from .conftest import DATA_DIR


def test():
    with tempfile.TemporaryDirectory() as temp_dir:
        # testing single file with output file option and without
        output_filename = os.path.join(temp_dir, "test.py")
        casefilename = os.path.join(DATA_DIR, "testcase", "secure-testcase.json")
        generate_test_backend([casefilename], output_filename)
        with open(output_filename, "rt") as f:
            file_text = f.read()
        stdout_text = generate_test_backend([casefilename], None)
        assert file_text == stdout_text
        assert "test_secure():" in file_text
        casefiles = [
            "secure-testcase.json",
            "insecure-testcase.json",
            "structure-good-testcase.json",
            "structure-bad-testcase.json",
            "invalid-syntax-testcase.json",
            "valid-syntax-testcase.json",
        ]
        # testing multiple files with output file option and without
        casefiles = list(
            map(lambda n: os.path.join(DATA_DIR, "testcase", n), casefiles)
        )
        generate_test_backend(casefiles, output_filename)
        with open(output_filename, "rt") as f:
            file_text = f.read()
        stdout_text = generate_test_backend(casefiles, None)
        assert file_text == stdout_text
        assert "test_secure():" in file_text
        assert "test_insecure():" in file_text
        assert "test_structureGood():" in file_text
        assert "test_structureBad():" in file_text
        assert "test_validSyntax():" in file_text
        assert "test_invalidSyntax():" in file_text

    # testing dir scan generation
    with tempfile.TemporaryDirectory() as temp_dir:
        copied_casefiles = []
        for filename in casefiles:
            filename = shutil.copy2(
                filename, os.path.join(temp_dir, os.path.basename(filename))
            )
            copied_casefiles.append(filename)
        assert generate_test_backend(copied_casefiles, None) == generate_test_backend(
            directory=temp_dir, output=None
        )

    # testing empty no testcase files error
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(BackendException) as einfo:
            generate_test_backend(directory=temp_dir, output=None)
        assert str(einfo.value) == "No testcase files found!"
        empty_testcase_file_path = os.path.join(temp_dir, "empty-testcase.json")
        with open(empty_testcase_file_path, "wt+") as f:
            json.dump({}, f)

        # testing empty testcase files error
        with pytest.raises(BackendException) as einfo:
            generate_test_backend(directory=temp_dir, output=None)
        assert str(einfo.value) == "No testcases found!"

        # testing extension check
        invalid_extension_filepath = os.path.join(temp_dir, "invalid.testcase.json")
        shutil.copy2(
            os.path.join(DATA_DIR, "testcase", "secure-testcase.json"),
            invalid_extension_filepath,
        )
        with pytest.raises(BackendException) as einfo:
            generate_test_backend(
                filenames=[invalid_extension_filepath], directory=None, output=None
            )
        assert (
            str(einfo.value)
            == f"Invalid extension for {invalid_extension_filepath}. Must be -testcase.json"
        )
