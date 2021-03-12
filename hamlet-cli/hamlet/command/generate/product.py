import click

from cookiecutter.exceptions import OutputDirExistsException

from hamlet.utils import dynamic_option, DynamicCommand
from hamlet.command.common.exceptions import CommandError
from hamlet.command.generate import utils
from hamlet.command.generate import decorators
from hamlet.backend.generate.product import django as generate_django_backend
from hamlet.backend.generate.product import base as generate_base_backend
from hamlet.backend.generate.product import app_lifecycle_mgmt as generate_app_lifecycle_mgmt_backend


@click.group('product')
def group():  # pragma: no cover
    pass


@group.command('base', cls=DynamicCommand)
@dynamic_option(
    '--product-id',
    help='The Id of your product',
    required=True,
)
@dynamic_option(
    '--dns-zone',
    help='A DNS zone name which will act as a base domain for public component hostnames',
    default='',
)
@dynamic_option(
    '--product-name',
    help='A more descriptive name of your product',
    default=lambda p: p.product_id,
)
@dynamic_option(
    '--environment-id',
    help='The id of your first deployed environment',
    default='int',
)
@dynamic_option(
    '--environment-name',
    help='A more descriptive name of your environment',
    default='integration',
)
@dynamic_option(
    '--segment-id',
    help='The id of the first segment in your environments',
    default='default',
)
@dynamic_option(
    '--segment-name',
    help='A more descriptive name of your segment',
    default=lambda p: p.segment_id,
)
@decorators.common_generate_options
@click.pass_context
def generate_base(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of a Hamlet product.
    This creates a base product with no deployed components.
    This template should be run from the root of an empty product directory.
    """
    if not prompt or utils.confirm(kwargs):
        try:
            generate_base_backend.run(**kwargs)
        except OutputDirExistsException as e:
            raise CommandError(e)


@group.command('app-lifecycle-mgmt', cls=DynamicCommand)
@dynamic_option('--product-id', required=True)
@dynamic_option('--product-name', default=lambda p: p.product_id)
@dynamic_option('--domain-id', default='')
@dynamic_option('--solution-id', default='alm')
@dynamic_option('--solution-name', default=lambda p: p.solution_id)
@dynamic_option('--environment-id', default='alm')
@dynamic_option('--environment-name', default=lambda p: p.environment_id)
@dynamic_option('--segment-id', default='default')
@dynamic_option('--segment-name', default=lambda p: p.segment_id)
@dynamic_option('--multi-az', is_flag=True)
@dynamic_option('--source-ip-network', default='0.0.0.0/0')
@dynamic_option('--certificate-arn', default='arn:aws:acm:us-east-1:123456789:certificate/replace-this-with-your-arn')
@dynamic_option('--certificate-cn', default='*.alm.local')
@dynamic_option('--certificate-region', default=lambda p: p.certificate_arn.split(':')[3])
@dynamic_option(
    '--slave-provider',
    type=click.Choice(
        [
            'ecs',
            'docker'
        ]
    ),
    default='ecs'
)
@dynamic_option('--ecs-instance-type', default=lambda p: 't3.medium' if p.slave_provider == 'ecs' else 'n/a')
@dynamic_option(
    '--security-realm',
    type=click.Choice(
        [
            'local',
            'github',
            'saml'
        ]
    ),
    default='local'
)
@dynamic_option(
    '--auth-local-user',
    default=lambda p: 'admin' if p.security_realm == 'local' else 'n/a',
    prompt=lambda p: p.security_realm == 'local'
)
@dynamic_option(
    '--auth-local-pass',
    default=lambda p: '' if p.security_realm == 'local' else 'n/a',
    prompt=lambda p: p.security_realm == 'local'
)
@dynamic_option(
    '--auth-github-client-id',
    default=lambda p: '' if p.security_realm == 'github' else 'n/a',
    prompt=lambda p: p.security_realm == 'github'
)
@dynamic_option(
    '--auth-github-secret',
    default=lambda p: '' if p.security_realm == 'github' else 'n/a',
    prompt=lambda p: p.security_realm == 'github'
)
@dynamic_option(
    '--auth-github-admin-role',
    default=lambda p: '' if p.security_realm == 'github' else 'n/a',
    prompt=lambda p: p.security_realm == 'github'
)
@dynamic_option('--github-repo-user', default='')
@dynamic_option('--github-repo-path', default='')
@decorators.common_generate_options
@click.pass_context
def generate_app_lifecycle_mgmt(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of a Hamlet product.
    This product provisions a container based application lifecycle management service used
    to build and deploy Hamlet managed applications.
    """
    if not prompt or utils.confirm(kwargs):
        try:
            generate_app_lifecycle_mgmt_backend.run(**kwargs)

        except OutputDirExistsException as e:
            raise CommandError(e)


@group.command('django', cls=DynamicCommand)
@dynamic_option('--product-id', required=True)
@dynamic_option('--product-name', default=lambda p: p.product_id)
@dynamic_option('--domain-id', default=lambda p: p.product_id)
@dynamic_option('--solution-id', default='app')
@dynamic_option('--solution-name', default=lambda p: p.solution_id)
@dynamic_option('--environment-id', default='int')
@dynamic_option('--environment-name', default='integration')
@dynamic_option('--environment-log-level', default='info')
@dynamic_option('--segment-id', default='default')
@dynamic_option('--segment-name', default=lambda p: p.segment_id)
@dynamic_option('--source-ip', default='_global')
@dynamic_option('--default-log-level', default='info')
@dynamic_option('--database-size-gb', type=click.INT, default=20)
@dynamic_option('--database-postgres-version', default='9.6')
@dynamic_option('--queue-redis-version', default='5.0.0')
@dynamic_option(
    '--container-placement-strategy',
    type=click.Choice(
        [
            'daemon',
            'replica'
        ]
    ),
    default='daemon'
)
@dynamic_option('--use-celery', is_flag=True)
@dynamic_option('--celery-flower-username', default='admin', prompt=lambda p: p.use_celery)
@dynamic_option('--email-from', default=lambda p: "%s - %s <noreply@local.host>" % (p.product_id, p.environment_name))
@dynamic_option('--email-server-from', default=lambda p: p.email_from)
@dynamic_option('--email-subject-prefix', default=lambda p: "%s - %s" % (p.product_id, p.environment_name))
@dynamic_option('--admin-url', default='admin/')
@dynamic_option('--loadbalancer-healthcheck-path', default='/healthcheck')
@dynamic_option('--loadbalancer-healthcheck-healthy-responsecode', default=200, type=click.INT)
@dynamic_option('--public-media-paths', default='static,media,CACHE')
@dynamic_option('--allow-user-registration', is_flag=True)
@dynamic_option('--sentry-dsn', default='')
@dynamic_option('--alerts-use-ktlg', is_flag=True)
@dynamic_option('--alerts-ktlg-hostname', default='', prompt=lambda p: p.alerts_use_ktlg)
@dynamic_option('--alerts-ktlg-channel', default='', prompt=lambda p: p.alerts_use_ktlg)
@dynamic_option('--alerts-ktlg-hex-colorcode', default='DC143C', prompt=lambda p: p.alerts_use_ktlg)
@dynamic_option('--alerts-use-email', is_flag=True, prompt=lambda p: p.alerts_use_ktlg)
@dynamic_option('--alerts-email-address', default='', prompt=lambda p: p.alerts_use_email)
@decorators.common_generate_options
@click.pass_context
def generate_django(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of an AWS based Django deployment. It includes all of the components
    required for a production level deployment of Django:

    - Web ECS Service for front end
    - Worker ECS Service for celery processing
    - Task ECS Task Definition for Django management
    - Postgres based RDS instance
    - Cloudfront S3 distribution for static content
    - Redis for queue management between web and worker
    - HTTPS offloading load balancer for web

    The template will create a single environment. If you want more you will need too add them manually.
    """

    if not prompt or utils.confirm(kwargs):
        try:
            generate_django_backend.run(**kwargs)

        except OutputDirExistsException as e:
            raise CommandError(e)
