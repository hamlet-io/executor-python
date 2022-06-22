from hamlet.backend.create import template as template_backend


def run(
    StackOutputContent,
    DeploymentUnit,
    DeploymentGroup,
    RootDir,
    Tenant,
    Account,
    Product,
    Environment,
    Segment,
    DistrictType,
    GenerationInputSource,
    GenerationProviders,
    GenerationFramework,
    env={},
):
    """
    Write a stack output file with the provided content
    """

    template_backend.run(
        entrance="stackoutput",
        entrance_parameter=(f"StackOutputContent={StackOutputContent}"),
        deployment_unit=DeploymentUnit,
        deployment_group=DeploymentGroup,
        deployment_mode="update",
        generation_provider=tuple(GenerationProviders.split(",")),
        generation_framework=GenerationFramework,
        generation_input_source=GenerationInputSource,
        district_type=DistrictType,
        root_dir=RootDir,
        tenant=Tenant,
        account=Account,
        environment=Environment,
        product=Product,
        segment=Segment,
        engine=env["_engine"],
        _is_cli=False,
    )

    return {"Properties": {}}
