from hamlet.backend.common import runner


def run(
    decrypt=None,
    encrypt=None,
    crypto_file=None,
    update=None,
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
    options = {"-d": decrypt, "-e": encrypt, "-f": crypto_file, "-u": update}
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
    runner.run(
        "manageFileCrypto.sh",
        args=[],
        options=options,
        env=env,
        engine=engine,
        _is_cli=_is_cli,
    )
