import tempfile

from hamlet.backend.common import runner


def run(
    deployment_group=None,
    deployment_unit=None,
    deployment_unit_subset=None,
    root_dir=None,
    tenant=None,
    district_type=None,
    account=None,
    product=None,
    environment=None,
    segment=None,
    output_dir=None,
    engine=None,
    _is_cli=False,
    **kwargs,
):
    with tempfile.NamedTemporaryFile() as output_file:

        env = {
            "ROOT_DIR": root_dir,
            "DISTRICT_TYPE": district_type,
            "TENANT": tenant,
            "ACCOUNT": account,
            "PRODUCT": product,
            "ENVIRONMENT": environment,
            "SEGMENT": segment,
            "DEPLOYMENT_UNIT": deployment_unit,
            "DEPLOYMENT_UNIT_SUBSET": deployment_unit_subset,
            "LEVEL": deployment_group,
            "OUTPUT_DIR": output_dir,
        }
        runner.run(
            "execution/common.sh",
            args=[],
            options={},
            env=env,
            engine=engine,
            _is_cli=_is_cli,
            script_base_path_env="GENERATION_BASE_DIR",
            extra_script='; . ${GENERATION_BASE_DIR}/execution/setStackContext.sh ; echo $CF_DIR > ' + output_file.name,
            source=True,
        )

        return open(output_file.name, "r").readline().strip()
