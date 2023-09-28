from hamlet.backend.common import runner


def run(
    account_repos=None,
    product_repos=None,
    commit_message=None,
    reference=None,
    tag=None,
    defer_push=None,
    log_level=None,
    root_dir=None,
    tenant=None,
    district_type=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    engine=None,
    _is_cli=False,
    env={},
    **kwargs,
):
    opts = {
        "-a": account_repos,
        "-m": commit_message,
        "-p": product_repos,
        "-r": reference,
        "-t": tag,
    }
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "DEFER_REPO_PUSH": defer_push,
        "ROOT_DIR": root_dir,
        "DISTRICT_TYPE": district_type,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
        **env,
    }
    runner.run(
        "saveCMDBRepos.sh",
        args=[],
        options=opts,
        env=env,
        engine=engine,
        _is_cli=_is_cli,
    )
