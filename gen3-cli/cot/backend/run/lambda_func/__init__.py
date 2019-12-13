from cot.backend.common import runner


def run(
    function_id=None,
    deployment_unit=None,
    input_payload=None,
    include_log_tail=None,
    _is_cli=False
):
    options = {
        '-f': function_id,
        '-u': deployment_unit,
        '-i': input_payload,
        '-l': include_log_tail
    }
    runner.run('runLambda.sh', [], options, _is_cli)
