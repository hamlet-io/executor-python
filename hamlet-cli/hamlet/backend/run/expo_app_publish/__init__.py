from hamlet.backend.common import runner


def run(
    deployment_unit=None,
    run_setup=None,
    binary_expiration=None,
    force_binary_build=None,
    submit_binary=None,
    disable_ota=None,
    binary_build_process=None,
    qr_build_formats=None,
    _is_cli=False
):
    options = {
        '-u': deployment_unit,
        '-s': run_setup,
        '-t': binary_expiration,
        '-f': force_binary_build,
        '-m': submit_binary,
        '-o': disable_ota,
        '-b': binary_build_process,
        '-q': qr_build_formats
    }
    runner.run('runExpoAppPublish.sh', [], options, _is_cli)
