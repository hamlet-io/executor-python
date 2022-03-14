from hamlet.backend.common import runner


def run(
    release_mode=None,
    acceptance_tag=None,
    deployment_unit=None,
    code_commit=None,
    code_tag=None,
    image_format=None,
    registry_scope=None,
    log_level=None,
    engine=None,
    _is_cli=False,
    env={},
):
    env = {
        "AUTOMATION_LOG_LEVEL": log_level,
        "DEPLOYMENT_UNIT_LIST": deployment_unit,
        "CODE_COMMIT": code_commit,
        "CODE_TAG": code_tag,
        "IMAGE_FORMAT": image_format,
        "REGISTRY_SCOPE": registry_scope,
        "RELEASE_MODE": release_mode,
        "ACCEPTANCE_TAG": acceptance_tag,
        **env,
    }
    runner.run(
        "confirmBuilds.sh",
        args=[],
        options={},
        env=env,
        engine=engine,
        _is_cli=_is_cli,
        script_base_path_env="AUTOMATION_DIR",
    )
