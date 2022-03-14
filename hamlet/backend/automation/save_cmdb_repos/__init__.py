from hamlet.backend.common import runner


def run(
    account_repos=None,
    product_repos=None,
    commit_message=None,
    reference=None,
    tag=None,
    defer_push=None,
    log_level=None,
    engine=None,
    _is_cli=False,
    env={},
):

    opts = {
        "-a": account_repos,
        "-m": commit_message,
        "-p": product_repos,
        "-r": reference,
        "-t": tag,
    }
    env = {"AUTOMATION_LOG_LEVEL": log_level, "DEFER_REPO_PUSH": defer_push, **env}
    runner.run(
        "saveCMDBRepos.sh",
        args=[],
        options=opts,
        env=env,
        engine=engine,
        _is_cli=_is_cli,
        script_base_path_env="AUTOMATION_DIR",
    )
