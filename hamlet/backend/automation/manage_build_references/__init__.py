from hamlet.backend.common import runner


def run(
    acceptance_tag=None,
    code_commits=None,
    list_full=None,
    segment_builds_dir=None,
    image_formats=None,
    list=None,
    registry_scopes=None,
    code_providers=None,
    code_repos=None,
    deployment_units=None,
    code_tags=None,
    update=None,
    verify=None,
    log_level=None,
    _is_cli=False,
    env={},
):
    opts = {
        "-a": acceptance_tag,
        "-c": code_commits,
        "-f": list_full,
        "-g": segment_builds_dir,
        "-i": image_formats,
        "-l": list,
        "-o": registry_scopes,
        "-p": code_providers,
        "-r": code_repos,
        "-s": deployment_units,
        "-t": code_tags,
        "-u": update,
        "-v": verify,
    }
    env = {"AUTOMATION_LOG_LEVEL": log_level, **env}
    runner.run(
        "manageBuildReferences.sh",
        [],
        opts,
        env,
        _is_cli,
        script_base_path_env="AUTOMATION_DIR",
    )
