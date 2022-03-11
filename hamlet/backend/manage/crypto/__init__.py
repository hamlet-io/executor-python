from hamlet.backend.common import runner


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
    log_level=None,
    log_format=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    engine=None,
    _is_cli=False,
    **kwargs,
):
    options = {
        "-a": alias,
        "-b": base64_decode,
        "-d": decrypt,
        "-e": encrypt,
        "-f": crypto_file,
        "-k": key_id,
        "-n": no_alteration,
        "-p": json_path,
        "-q": quiet,
        "-t": crypto_text,
        "-u": update,
        "-v": visible,
    }
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "GENERATION_LOG_FORMAT": log_format,
        "ROOT_DIR": root_dir,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run("manageCrypto.sh", [], options, engine, env, _is_cli)
