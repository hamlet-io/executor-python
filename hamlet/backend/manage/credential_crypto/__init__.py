from hamlet.backend.common import runner


def run(
    credential_email=None,
    crypto_file=None,
    credential_id=None,
    credential_path=None,
    credential_secret=None,
    visible=None,
    credential_type=None,
    log_level=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
    **kwargs,
):
    options = {
        "-e": credential_email,
        "-f": crypto_file,
        "-i": credential_id,
        "-n": credential_path,
        "-v": visible,
        "-y": credential_type,
        "-s": credential_secret,
    }
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "ROOT_DIR": root_dir,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run("manageCredentialCrypto.sh", [], options, env, _is_cli)
