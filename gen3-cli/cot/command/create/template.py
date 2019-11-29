import click
from cot.backend.create import template as create_template_backend


@click.command(
    'template',
    short_help='Create a CloudFormation (CF) template',
    context_settings=dict(
        max_content_width=240
    )
)
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
            "account",
            "segment",
            "solution",
            "application"
        ],
        case_sensitive=False
    ),
    required=True
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
    help='deployment unit to be included in the template',
    required=True
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
@click.option(
    '-i',
    '--generation-input-source',
    help='source of input data to use when generating the template'
)
def template(**kwargs):
    """
    Create a CloudFormation (CF) template

    \b
    1. You must be in the directory specific to the level
    2. REGION is only relevant for the "product" level
    3. DEPLOYMENT_UNIT must be one of "s3", "cert", "roles", "apigateway" or "waf" for the "account" level
    4. DEPLOYMENT_UNIT must be one of "cmk", "cert", "sns" or "shared" for the "product" level
    5. For the "segment" level the "baseline" unit must be deployed before any other unit
    6. When deploying network level components in the "segment" level you must deploy vpc before
    igw, nat, or vpcendpoint

    """
    create_template_backend.run(**kwargs, _is_cli=True)
