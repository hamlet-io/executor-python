from hamlet.backend.common import runner


def run(
    _is_cli=False
):
    options = {}
    runner.run('setup.sh', [], options, _is_cli)
