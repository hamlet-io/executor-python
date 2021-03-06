from hamlet.backend.common import runner


def run(
    generation_input_source=None,
    output_dir=None,
    generation_provider=None,
    generation_framework=None,
    generation_testcase=None,
    _is_cli=False
):
    options = {
        '-i': generation_input_source,
        '-o': output_dir,
        '-p': generation_provider,
        '-f': generation_framework,
        '-t': generation_testcase,
        '-l': 'unitlist'
    }
    runner.run('createTemplate.sh', [], options, _is_cli)
