import click
from cot import utils
from cot.backend.generate.product import django as generate_django_backend
from cot.backend.generate.product import base as generate_base_backend
from cot.backend.generate.product import app_lifecycle_mgmt as generate_app_lifecycle_mgmt_backend


@click.group('product')
def group():
    pass


@click.option(
    '--product-id'
)
@click.option(
    '--product-name'
)
@click.option(
    '--domain-id'
)
@click.option(
    '--solution-id'
)
@click.option(
    '--solution-name'
)
@click.option(
    '--environment-id'
)
@click.option(
    '--environment-name'
)
@click.option(
    '--segment-id'
)
@click.option(
    '--segment-name'
)
@click.option(
    '--use-default',
    is_flag=True
)
@click.option(
    '--prompt',
    is_flag=True
)
@click.pass_context
@group.command('base')
def generate_base(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of a codeontap product.
    This creates a base product with no deployed components.
    This template should be run from the root of an empty product directory.
    """
    if not prompt:
        generate_base_backend.run(**kwargs)
        return

    prompt = utils.ClickMissingOptionsPrompt(ctx, kwargs, use_default)

    prompt.product_id()
    prompt.product_name(default=kwargs['product_id'])
    prompt.domain_id(default=kwargs['product_id'])

    prompt.solution_id(default='app')
    prompt.solution_name(default=kwargs['solution_id'])

    prompt.environment_id(default='int')
    prompt.environment_name(default='integration')

    prompt.segment_id(default='default')
    prompt.segment_name(default=kwargs['segment_id'])

    if prompt.confirm():
        generate_base_backend.run(**kwargs)


@group.command('app-lifecycle-mgmt')
@click.option(
    '--product-id'
)
@click.option(
    '--product-name'
)
@click.option(
    '--domain-id'
)
@click.option(
    '--solution-id'
)
@click.option(
    '--solution-name'
)
@click.option(
    '--environment-id'
)
@click.option(
    '--environment-name'
)
@click.option(
    '--segment-id'
)
@click.option(
    '--segment-name'
)
@click.option(
    '--multi-az',
    type=click.BOOL
)
@click.option(
    '--source-ip-network'
)
@click.option(
    '--certificate-arn'
)
@click.option(
    '--certificate-cn'
)
@click.option(
    '--certificate-region'
)
@click.option(
    '--slave-provider'
)
@click.option(
    '--ecs_instance_type'
)
@click.option(
    '--security-realm'
)
@click.option(
    '--auth-local-user'
)
@click.option(
    '--auth-local-pass'
)
@click.option(
    '--auth-github-client-id'
)
@click.option(
    '--auth-github-secret'
)
@click.option(
    '--auth-github-admin-role'
)
@click.option(
    '--github-repo-user'
)
@click.option(
    '--github-repo-path'
)
@click.option(
    '--use-default',
    is_flag=True
)
@click.option(
    '--prompt',
    is_flag=True
)
@click.pass_context
def generate_app_lifecycle_mgmt(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of a codeontap product.
    This product provisions a container based application lifecycle management service used
    to build and deploy codeontap managed applications.
    """
    if not prompt:
        generate_app_lifecycle_mgmt_backend.run(**kwargs)
        return

    prompt = utils.ClickMissingOptionsPrompt(ctx, kwargs, use_default)

    prompt.product_id()
    prompt.product_name(default=kwargs['product_id'])
    prompt.domain_id(default=kwargs['product_id'])

    prompt.solution_id(default='alm')
    prompt.solution_name(default=kwargs['solution_id'])

    prompt.environment_id(default='alm')
    prompt.environment_name(default=kwargs['environment_id'])

    prompt.segment_id(default='default')
    prompt.segment_name(default=kwargs['segment_id'])

    prompt.multi_az(default=False)
    prompt.source_ip_network(default='0.0.0.0/0')
    prompt.certificate_arn(default='arn:aws:acm:us-east-1:123456789:certificate/replace-this-with-your-arn')
    prompt.certificate_cn(default='*.alm.local')
    prompt.certificate_region(default=kwargs['certificate_arn'].split(':')[3])
    prompt.slave_provider()
    prompt.ecs_instance_type(default='t3.medium' if kwargs['slave_provider'] == 'ecs' else 'n/a')
    prompt.security_realm()
    prompt.auth_local_user(default='admin' if kwargs['security_realm'] == 'local' else 'n/a')
    prompt.auth_local_pass(default='' if kwargs['security_realm'] == 'local' else 'n/a')
    prompt.auth_github_client_id(default='' if kwargs['security_realm'] == 'github' else 'n/a')
    prompt.auth_github_secret(default='' if kwargs['security_realm'] == 'github' else 'n/a')
    prompt.auth_github_admin_role(default='' if kwargs['security_realm'] == 'github' else 'n/a')
    prompt.github_repo_user()
    prompt.github_repo_pass()
    if prompt.confirm():
        generate_app_lifecycle_mgmt_backend.run(**kwargs)


@group.command('django')
@click.option(
    '--product-id'
)
@click.option(
    '--product-name'
)
@click.option(
    '--domain-id'
)
@click.option(
    '--solution-id'
)
@click.option(
    '--solution-name'
)
@click.option(
    '--environment-id'
)
@click.option(
    '--environment-name'
)
@click.option(
    '--environment-log-level'
)
@click.option(
    '--segment-id'
)
@click.option(
    '--segment-name'
)
@click.option(
    '--source-ip'
)
@click.option(
    '--default-log-level'
)
@click.option(
    '--database-size-gb'
)
@click.option(
    '--database-postgres-version'
)
@click.option(
    '--queue-redis-version'
)
@click.option(
    '--container-placement-strategy',
    type=click.Choice(
        [
            'daemon',
            'replica'
        ]
    )
)
@click.option(
    '--use-celery',
    type=click.BOOL
)
@click.option(
    '--celery-flower-username'
)
@click.option(
    '--email-from'
)
@click.option(
    '--email-server-from'
)
@click.option(
    '--email-subject-prefix'
)
@click.option(
    '--admin-url'
)
@click.option(
    '--loadbalancer-healthcheck-path'
)
@click.option(
    '--loadbalancer-healthcheck-healthy-responsecode'
)
@click.option(
    '--public-media-paths'
)
@click.option(
    '--allow-user-registration',
    type=click.BOOL
)
@click.option(
    '--sentry-dsn'
)
@click.option(
    '--alerts-use-ktlg',
    type=click.BOOL
)
@click.option(
    '--alerts-ktlg-hostname'
)
@click.option(
    '--alerts-ktlg-channel'
)
@click.option(
    '--alerts-ktlg-hex-colorcode'
)
@click.option(
    '--alerts-use-email',
    type=click.BOOL
)
@click.option(
    '--alerts-email-address'
)
@click.option(
    '--use-default',
    is_flag=True
)
@click.option(
    '--prompt',
    is_flag=True
)
@click.pass_context
def generate_django(
    ctx,
    prompt=None,
    use_default=None,
    **kwargs
):
    """
    This template is for the creation of an AWS based Django deployment. It includes all of the components
    required for a produciton level deployment of Django:

    - Web ECS Service for front end
    - Worker ECS Service for celery processing
    - Task ECS Task Definition for Django management
    - Postgres based RDS instance
    - Cloudfront S3 distribution for static content
    - Redis for queue management between web and worker
    - HTTPS offloading load balancer for web

    The template will create a single environment. If you want more you will need too add them manually.
    """

    if not prompt:
        generate_django_backend.run(**kwargs)
        return

    prompt = utils.ClickMissingOptionsPrompt(ctx, kwargs, use_default)
    prompt.product_id()
    prompt.product_name(default=kwargs['product_id'])
    prompt.domain_id(default=kwargs['product_id'])

    prompt.solution_id(default='app')
    prompt.solution_name(default=kwargs['solution_id'])

    prompt.environment_id(default='int')
    prompt.environment_name(default='integration')
    prompt.environment_log_level(default='info')

    prompt.segment_id(default='default')
    prompt.segment_name(default=kwargs['segment_id'])

    prompt.source_ip(default='_global')

    prompt.default_log_level(default='info')

    prompt.database_size_gb(default=20)
    prompt.database_postgres_version(default='9.6')
    prompt.queue_redis_version(default='5.0.0')

    prompt.container_placement_strategy()

    if prompt.use_celery():
        prompt.celery_flower_username(default='admin')

    prompt.email_from(default="{} - {} <noreply@local.host>".format(kwargs['product_id'], kwargs['environment_name']))
    prompt.email_server_from(default=kwargs['email_from'])
    prompt.email_subject_prefix(default="{} - {}".format(kwargs['product_id'], kwargs['environment_name']))

    prompt.admin_url(default='admin/')

    prompt.loadbalancer_healthcheck_path(default='/healthcheck')
    prompt.loadbalancer_healthcheck_healthy_responsecode(default=200)
    prompt.public_media_paths(default='static,media,CACHE')

    prompt.allow_user_registration()

    prompt.sentry_dsn()

    if prompt.alerts_use_ktlg():
        prompt.alerts_ktlg_hostname()
        prompt.alerts_ktlg_channel()
        prompt.alerts_ktlg_hex_colorcode(default='DC143C')
        if prompt.alerts_use_email():
            prompt.alerts_email_address()

    if prompt.confirm():
        generate_django_backend.run(**kwargs)
