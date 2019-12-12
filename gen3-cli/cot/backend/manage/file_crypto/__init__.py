from cot.backend.common import runner


def run(
    decrypt=None,
    encrypt=None,
    crypto_file=None,
    update=None,
    _is_cli=False
):
    options = {
        '-d': decrypt,
        '-e': encrypt,
        '-f': crypto_file,
        '-u': update
    }
    runner.run('manageFileCrypto.sh', [], options, _is_cli)
