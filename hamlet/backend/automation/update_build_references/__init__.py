from hamlet.backend.common import runner


def run(
    log_level=None,
    deployment_unit=None,
    code_commit=None,
    code_tag=None,
    image_format=None,
    registry_scope=None,
    engine=None,
    _is_cli=False,
    env={},
):
    env = {
        "AUTOMATION_LOG_LEVEL": log_level,
        "DEPLOYMENT_UNITS": deployment_unit,
        "CODE_COMMIT": code_commit,
        "CODE_TAG": code_tag,
        "IMAGE_FORMATS": image_format,
        "REGISTRY_SCOPE": registry_scope,
        **env,
    }
    runner.run(
        "updateBuildReferences.sh",
        args=[],
        options={},
        env=env,
        engine=engine,
        _is_cli=_is_cli,
        script_base_path_env="AUTOMATION_DIR",
    )
