import collections
from unittest import mock
from click.testing import CliRunner
from cot.command.generate.product import generate_django
from tests.unit.command.generate.test_generate_command import run_generate_command_test

OPTIONS = collections.OrderedDict()
OPTIONS['!--product-id,product_id'] = 'test-product-id'
OPTIONS['--product-name,product_name'] = ('test-product-name', 'test-product-id')
OPTIONS['--domain-id,domain_id'] = ('test-domain-id', 'test-product-id')
OPTIONS['--solution-id,solution_id'] = ('test-solution-id', 'app')
OPTIONS['--solution-name,solution_name'] = ('test-solution-name', 'app')
OPTIONS['--environment-id,environment_id'] = ('test-environment-id', 'int')
OPTIONS['--environment-name,environment_name'] = ('test-environment-name', 'integration')
OPTIONS['--environment-log-level,environment_log_level'] = ('debug', 'info')
OPTIONS['--segment-id,segment_id'] = ('test-segment-id', 'default')
OPTIONS['--segment-name,segment_name'] = ('test-segment-name', 'default')
OPTIONS['--source-ip,source_ip'] = ('_local', '_global')
OPTIONS['--default-log-level,default_log_level'] = ('debug', 'info')
OPTIONS['--database-size-gb,database_size_gb'] = (10, 20)
OPTIONS['--database-postgres-version,database_postgres_version'] = ('10.0.0', '9.6')
OPTIONS['--queue-redis-version,queue_redis_version'] = ('6.0.0', '5.0.0')
OPTIONS['--container-placement-strategy,container_placement_strategy'] = ('replica', 'daemon')
OPTIONS['--use-celery,use_celery'] = (True, False)
OPTIONS['--celery-flower-username,celery_flower_username'] = ('root', 'admin')
OPTIONS['--email-from,email_from'] = ('test@email.com', 'test-product-id - integration <noreply@local.host>')
OPTIONS['--email-server-from,email_server_from'] = (
    'server@email.com',
    'test-product-id - integration <noreply@local.host>'
)
OPTIONS['--email-subject-prefix,email_subject_prefix'] = ('subject_prefix', 'test-product-id - integration')
OPTIONS['--admin-url,admin_url'] = ('administrator/', 'admin/')
OPTIONS['--loadbalancer-healthcheck-path,loadbalancer_healthcheck_path'] = ('/health', '/healthcheck')
OPTIONS['--loadbalancer-healthcheck-healthy-responsecode, loadbalancer_healthcheck_healthy_responsecode'] = (
    201,
    200
)
OPTIONS['--public-media-paths,public_media_paths'] = ('static', 'static,media,CACHE')
OPTIONS['--allow-user-registration,allow_user_registration'] = (True, False)
OPTIONS['--sentry-dsn,sentry_dsn'] = ('sentry_dsn', '')
OPTIONS['--alerts-use-ktlg,alerts_use_ktlg'] = (True, False)
OPTIONS['--alerts-ktlg-hostname,alerts_ktlg_hostname'] = ('hostname', '')
OPTIONS['--alerts-ktlg-channel,alerts_ktlg_channel'] = ('channel', '')
OPTIONS['--alerts-ktlg-hex-colorcode, alerts_ktlg_hex_colorcode'] = ('00000', 'DC143C')
OPTIONS['--alerts-use-email,alerts_use_email'] = (True, False)
OPTIONS['--alerts-email-address,alerts_email_address'] = ('alerts@email.com', '')


@mock.patch('cot.command.generate.product.generate_django_backend')
def test(generate_django_backend):
    run_generate_command_test(
        CliRunner(),
        generate_django,
        generate_django_backend.run,
        OPTIONS
    )
