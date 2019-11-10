import os
import subprocess
import click
from cot import env
from cot import utils


@click.command(context_settings=dict(max_content_width=240))
@click.option(
    '-c',
    '--config-ref',
    help='identifier of the configuration used to generate this template',
    default='unassigned',
    show_default=True
)
@click.option(
    '-g',
    '--resource-group',
    help='deployment unit resource group',
)
@click.option(
    '-l',
    '--level',
    help='template level',
    type=click.Choice(
        [
            "blueprint",
            "account",
            "segment",
            "solution",
            "application"
        ],
        case_sensitive=False
    )
)
@click.option(
    '-q',
    '--request-ref',
    help='opaque value to link this template to a triggering request management system',
    default='unassigned',
    show_default=True
)
@click.option(
    '-r',
    '--region'
)
@click.option(
    '-u',
    '--deployment-unit',
    help='deployment unit to be included in the template'
)
@click.option(
    '-z',
    '--deployment-unit-subset',
    help='subset of the deployment unit required'
)
@click.option(
    '-d',
    '--deployment-mode',
    help='deployment mode the template will be generated for',
    default='update',
    show_default=True
)
@click.option(
    '-p',
    '--generation-provider',
    help='provider to for template generation',
    default='aws',
    show_default=True
)
@click.option(
    '-f',
    '--generation-framework',
    help='output framework to use for template generation',
    default='cf',
    show_default=True
)
@click.option(
    '-t',
    '--generation-testcase',
    help='test case you would like to generate a template for'
)
@click.option(
    '-s',
    '--generation-scenarios',
    help='comma seperated list of framework scenarios to load'
)
def template(
    config_ref,
    resource_group,
    level,
    request_ref,
    region,
    deployment_unit,
    deployment_unit_subset,
    deployment_mode,
    generation_provider,
    generation_framework,
    generation_testcase,
    generation_scenarios
):
    """
    Create a CloudFormation (CF) template

    \b
    1. You must be in the directory specific to the level
    2. REGION is only relevant for the "product" level
    3. DEPLOYMENT_UNIT must be one of "s3", "cert", "roles", "apigateway" or "waf" for the "account" level
    4. DEPLOYMENT_UNIT must be one of "cmk", "cert", "sns" or "shared" for the "product" level
    5. For the "segment" level the "baseline" unit must be deployed before any other unit
    6. When deploying network level components in the "segment" level you must deploy vpc before igw, nat, or vpcendpoint

    """
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
        '-s': generation_scenarios
    }
    script_call_line = utils.cli_params_to_script_call(
        env.GENERATION_DIR,
        'createTemplate.sh',
        args=[],
        options=options
    )
    subprocess.run(
        script_call_line,
        shell=True
    )
