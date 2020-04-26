from hamlet.backend.common import runner


def run(
    config_ref=None,
    resource_group=None,
    level=None,
    request_ref=None,
    region=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    deployment_mode=None,
    generation_provider=None,
    generation_framework=None,
    generation_testcase=None,
    generation_scenarios=None,
    generation_input_source=None,
    output_dir=None,
    _is_cli=False
):
    options = {
        '-c': config_ref,
        '-g': resource_group,
        '-l': level,
        '-q': request_ref,
        '-r': region,
        '-u': deployment_unit,
        '-z': deployment_unit_subset,
        '-d': deployment_mode,
        '-p': generation_provider,
        '-f': generation_framework,
        '-t': generation_testcase,
        '-s': generation_scenarios,
        '-i': generation_input_source,
        '-o': output_dir
    }
    runner.run('createTemplate.sh', [], options, _is_cli)
