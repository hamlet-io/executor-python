from cot.backend.common import runner


def run(
    generation_input_source=None,
    output_dir=None,
    generation_provider=None,
    generation_framework=None,
    generation_testcase=None,
    generation_scenarios=None,
    deployment_unit=None,
    _is_cli=False
):
    options = {
        '-i': generation_input_source,
        '-o': output_dir,
        '-p': generation_provider,
        '-f': generation_framework,
        '-t': generation_testcase,
        '-s': generation_scenarios,
        '-u': deployment_unit
    }
    runner.run('createBuildblueprint.sh', [], options, _is_cli)
