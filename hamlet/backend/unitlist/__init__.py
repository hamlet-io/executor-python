from hamlet.backend.common import runner


def run(
    generation_input_source=None,
    output_dir=None,
    generation_provider=None,
    generation_framework=None,
    generation_testcase=None,
    log_level=None,
    root_dir=None,
    tenant=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    _is_cli=False,
):
    options = {
        "-i": generation_input_source,
        "-o": output_dir,
        "-p": generation_provider,
        "-f": generation_framework,
        "-t": generation_testcase,
        "-l": "unitlist",
    }
    env = {
        "GENERATION_LOG_LEVEL": log_level,
        "ROOT_DIR": root_dir,
        "TENANT": tenant,
        "ACCOUNT": account,
        "PRODUCT": product,
        "ENVIRONMENT": environment,
        "SEGMENT": segment,
    }
    runner.run("createTemplate.sh", [], options, env, _is_cli)
