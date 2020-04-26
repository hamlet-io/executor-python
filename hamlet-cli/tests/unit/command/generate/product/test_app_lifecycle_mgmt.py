import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.generate.product import generate_app_lifecycle_mgmt
from tests.unit.command.generate.test_generate_command import run_generate_command_test

OPTIONS = collections.OrderedDict()
OPTIONS['!--product-id,product_id'] = 'test-product-id'
OPTIONS['--product-name,product_name'] = ('test-product-name', 'test-product-id')
OPTIONS['--domain-id,domain_id'] = ('test-domain-id', '')
OPTIONS['--solution-id,solution_id'] = ('test-solution-id', 'alm')
OPTIONS['--solution-name,solution_name'] = ('test-solution-name', 'alm')
OPTIONS['--environment-id,environment_id'] = ('test-environment-id', 'alm')
OPTIONS['--environment-name,environment_name'] = ('test-environment-name', 'alm')
OPTIONS['--segment-id,segment_id'] = ('test-segment-id', 'default')
OPTIONS['--segment-name,segment_name'] = ('test-segment-name', 'default')
OPTIONS['--multi-az,multi_az'] = (True, False)
OPTIONS['--source-ip-network,source_ip_network'] = ('1.1.1.1/1', '0.0.0.0/0')
OPTIONS['--certificate-arn,certificate_arn'] = (
    'arn:aws:acm:us-west-1:123456789:certificate/replace-this-with-your-arn',
    'arn:aws:acm:us-east-1:123456789:certificate/replace-this-with-your-arn'
)
OPTIONS['--certificate-cn,certificate_cn'] = ('*.alm.global', '*.alm.local')
OPTIONS['--certificate-region,certificate_region'] = ('us-west-1', 'us-east-1')
OPTIONS['--slave-provider,slave_provider'] = ('docker', 'ecs')
OPTIONS['--ecs-instance-type,ecs_instance_type'] = ('n/a', 't3.medium')
OPTIONS['--security-realm,security_realm'] = ('github', 'local')
OPTIONS['--auth-local-user,auth_local_user'] = ('n/a', 'admin')
OPTIONS['--auth-local-pass,auth_local_pass'] = ('n/a', '')
OPTIONS['--auth-github-client-id,auth_github_client_id'] = ('github-client-id', 'n/a')
OPTIONS['--auth-github-secret,auth_github_secret'] = ('github-secret', 'n/a')
OPTIONS['--auth-github-admin-role,auth_github_admin_role'] = ('github-admin-role', 'n/a')
OPTIONS['--github-repo-user,github_repo_user'] = ('github-repo-user', '')
OPTIONS['--github-repo-path,github_repo_path'] = ('github-repo-path', '')


@mock.patch('hamlet.command.generate.product.generate_app_lifecycle_mgmt_backend')
def test(generate_app_lifecycle_mgmt_backend):
    run_generate_command_test(
        CliRunner(),
        generate_app_lifecycle_mgmt,
        generate_app_lifecycle_mgmt_backend.run,
        OPTIONS
    )
