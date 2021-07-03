from hamlet.backend.generate.cmdb import account


conf = dict(
    cmdb=dict(
        tenant=dict(
            tenant_id="tenant_id",
            tenant_name="tenant",
            domain_stem="codeontap.io",
            default_region="ap-southeast-2",
            audit_log_expiry_days=2555,
            audit_log_offline_days=90,
        ),
        account=dict(
            account_id="account_id",
            account_name="account",
            account_seed=account.generate_account_seed(),
            account_type="aws",
            aws_account_id="",
        ),
        product=dict(
            product_id="product_id",
            product_name="product",
            dns_zone="product.local",
            environment_id="environment_id",
            environment_name="environment",
            segment_id="segment_id",
            segment_name="segment",
        ),
    )
)
