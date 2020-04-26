from hamlet.backend.common import runner


def run(
    credential_email=None,
    crypto_file=None,
    credential_id=None,
    credential_path=None,
    credential_secret=None,
    visible=None,
    credential_type=None,
    _is_cli=False
):
    options = {
        '-e': credential_email,
        '-f': crypto_file,
        '-i': credential_id,
        '-n': credential_path,
        '-v': visible,
        '-y': credential_type,
        '-s': credential_secret
    }
    runner.run('manageCredentialCrypto.sh', [], options, _is_cli)
