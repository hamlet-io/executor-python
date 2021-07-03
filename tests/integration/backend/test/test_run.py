import os
import tempfile
from pytest import raises
from hamlet.backend.test.run import run as run_test_backend
from hamlet.backend.test.generate import run as generate_test_backend
from .conftest import DATA_DIR


def test():
    with tempfile.TemporaryDirectory() as dir:
        output_filename = os.path.join(dir, "test.py")

        def testcase_filename(name):
            return os.path.join(DATA_DIR, "testcase", name)

        generate_test_backend(
            [testcase_filename("secure-testcase.json")], output_filename
        )
        assert run_test_backend([output_filename])
        generate_test_backend(
            [testcase_filename("insecure-testcase.json")], output_filename
        )
        with raises(Exception) as e:
            run_test_backend([output_filename])
            assert e.message == "Tests Failed"

        generate_test_backend(
            [testcase_filename("valid-syntax-testcase.json")], output_filename
        )
        assert run_test_backend([output_filename])
        generate_test_backend(
            [testcase_filename("invalid-syntax-testcase.json")], output_filename
        )
        with raises(Exception) as e:
            run_test_backend([output_filename])
            assert e.message == "Tests Failed"

        generate_test_backend(
            [testcase_filename("structure-good-testcase.json")], output_filename
        )
        assert run_test_backend([output_filename])
        generate_test_backend(
            [testcase_filename("structure-bad-testcase.json")], output_filename
        )
        with raises(Exception) as e:
            run_test_backend([output_filename])
            assert e.message == "Tests Failed"

        generate_test_backend(
            [testcase_filename("json-structure-good-testcase.json")], output_filename
        )
        assert run_test_backend([output_filename])
        generate_test_backend(
            [testcase_filename("json-structure-bad-testcase.json")], output_filename
        )
        with raises(Exception) as e:
            run_test_backend([output_filename])
            assert e.message == "Tests Failed"
