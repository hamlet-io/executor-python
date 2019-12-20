import os
import tempfile
from cot.backend.test.run import run as run_test_backend
from cot.backend.test.generate import run as generate_test_backend
from .conftest import DATA_DIR


def test():
    with tempfile.TemporaryDirectory() as dir:
        output_filename = os.path.join(dir, 'test.py')

        def testcase_filename(name):
            return os.path.join(DATA_DIR, 'testcase', name)

        generate_test_backend([testcase_filename('secure.json')], output_filename)
        assert run_test_backend(output_filename)
        generate_test_backend([testcase_filename('insecure.json')], output_filename)
        assert not run_test_backend(output_filename)

        generate_test_backend([testcase_filename('valid-syntax.json')], output_filename)
        assert run_test_backend(output_filename)
        generate_test_backend([testcase_filename('invalid-syntax.json')], output_filename)
        assert not run_test_backend(output_filename)

        generate_test_backend([testcase_filename('structure-good.json')], output_filename)
        assert run_test_backend(output_filename)
        generate_test_backend([testcase_filename('structure-bad.json')], output_filename)
        assert not run_test_backend(output_filename)