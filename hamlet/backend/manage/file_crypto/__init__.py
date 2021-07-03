from hamlet.backend.common import runner


def run(
    decrypt=None,
    encrypt=None,
    crypto_file=None,
    update=None,
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
    options = {"-d": decrypt, "-e": encrypt, "-f": crypto_file, "-u": update}
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "ROOT_DIR": root_dir,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run("manageFileCrypto.sh", [], options, env, _is_cli)
