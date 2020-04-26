from hamlet.backend.common import runner


def run(
    reference_type=None,
    reference_output_dir=None,
    _is_cli=False
):
    options = {
        '-t': reference_type,
        '-o': reference_output_dir
    }
    runner.run('createReference.sh', [], options, _is_cli)
