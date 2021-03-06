from hamlet.backend.common import runner


def run(
    entrance=None,
    config_ref=None,
    resource_group=None,
    request_ref=None,
    region=None,
    deployment_group=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    deployment_mode=None,
    generation_provider=None,
    generation_framework=None,
    generation_input_source=None,
    output_dir=None,
    disable_output_cleanup=None,
    _is_cli=False
):
    options = {
        '-e': entrance,
        '-c': config_ref,
        '-g': resource_group,
        '-l': deployment_group,
        '-q': request_ref,
        '-r': region,
        '-u': deployment_unit,
        '-z': deployment_unit_subset,
        '-d': deployment_mode,
        '-p': generation_provider,
        '-f': generation_framework,
        '-i': generation_input_source,
        '-o': output_dir,
        '-x': disable_output_cleanup
    }
    runner.run('createTemplate.sh', [], options, _is_cli)
