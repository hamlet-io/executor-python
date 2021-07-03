from hamlet.backend.generate.cmdb import account


conf = dict(
    cmdb=dict(
        tenant=dict(
            tenant_id="test_tenant_id",
            tenant_name="test_tenant_name",
            domain_stem="codeontap.io",
            default_region="ap-southeast-2",
            audit_log_expiry_days=2555,
            audit_log_offline_days=90,
        ),
        account=dict(
            account_id="test_account_id",
            account_name="test_account_name",
            account_seed=account.generate_account_seed(),
            account_type="aws",
            aws_account_id="",
        ),
        product=dict(
            product_id="base_product_id",
            product_name="base_product_name",
            domain_id="base.domain.id",
            solution_id="base_solution_id",
            solution_name="solution",
            environment_id="environment_id",
            environment_name="environment_name",
            segment_id="segment_id",
            segment_name="segment_name",
        ),
    )
)
