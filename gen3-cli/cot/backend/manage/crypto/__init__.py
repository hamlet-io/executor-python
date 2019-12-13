from cot.backend.common import runner


def run(
    alias=None,
    base64_decode=None,
    decrypt=None,
    encrypt=None,
    crypto_file=None,
    key_id=None,
    no_alteration=None,
    json_path=None,
    quiet=None,
    crypto_text=None,
    update=None,
    visible=None,
    _is_cli=False
):
    options = {
        '-a': alias,
        '-b': base64_decode,
        '-d': decrypt,
        '-e': encrypt,
        '-f': crypto_file,
        '-k': key_id,
        '-n': no_alteration,
        '-p': json_path,
        '-q': quiet,
        '-t': crypto_text,
        '-u': update,
        '-v': visible
    }
    runner.run('manageCrypto.sh', [], options, _is_cli)
