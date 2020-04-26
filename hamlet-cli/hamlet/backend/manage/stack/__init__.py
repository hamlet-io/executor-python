from hamlet.backend.common import runner


def run(
    delete=None,
    stack_initiate=None,
    stack_monitor=None,
    stack_wait=None,
    stack_name=None,
    level=None,
    region=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    dryrun=None,
    _is_cli=False
):
    options = {
        '-d': delete,
        '-i': stack_initiate,
        '-m': stack_monitor,
        '-w': stack_wait,
        '-n': stack_name,
        '-r': region,
        '-y': dryrun,
        '-u': deployment_unit,
        '-z': deployment_unit_subset,
        '-l': level
    }
    runner.run('manageStack.sh', [], options, _is_cli)
