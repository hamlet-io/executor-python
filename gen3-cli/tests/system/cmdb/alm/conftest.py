from cot.backend.generate.cmdb import account


conf = dict(
    cmdb=dict(
        tenant=dict(
            tenant_id='tenant_id',
            tenant_name='tenant',
            domain_stem='codeontap.io',
            default_region='ap-southeast-2',
            audit_log_expiry_days=2555,
            audit_log_offline_days=90
        ),
        account=dict(
            account_id='account_id',
            account_name='account',
            account_seed=account.generate_account_seed(),
            account_type='aws',
            aws_account_id=''
        ),
        product=dict(
            product_id='alm_product_id',
            product_name='automation',
            domain_id='alm.domain.id',
            solution_id='alm_solution_id',
            solution_name='solution',
            environment_id='environment_id',
            environment_name='environment',
            segment_id='segment_id',
            segment_name='segment',
            multi_az=True,
            source_ip_network='0.0.0.0/0',
            certificate_arn='arn:aws:acm:us-east-1:123456789:certificate/replace-this-with-your-arn',
            certificate_cn='*.alm.local',
            certificate_region='us-east-1',
            slave_provider='ecs',
            ecs_instance_type='t3.medium',
            security_realm='local',
            auth_local_user='admin',
            auth_local_path='',
            auth_github_client_id='n/a',
            auth_github_secret='n/a',
            auth_github_admin_role='n/a',
            github_repo_user='',
            github_repo_path=''
        )
    )
)
