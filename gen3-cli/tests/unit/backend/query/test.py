import os
import json
import tempfile
from unittest import mock
from cot.backend import query


BLUEPRINT_JSON = {
    "Tenants": [
        {
            "Id": "Tenant-Id",
            "Products": [
                {
                    "Environments": [
                        {
                            "Segments": [
                                {
                                    "Tiers": [
                                        {
                                            "Id": "Tier-1-Id",
                                            "Configuration": {
                                                "Name": "Tier-1-Name",
                                                "Description": "Tier-1-Description",
                                                "Network": {
                                                    "Enabled": False
                                                }
                                            },
                                            "Components": [
                                                {
                                                    "Id": "Component-1-Id",
                                                    "Name": "Component-1-Name",
                                                    "Type": "Component-1-Type"
                                                },
                                                {
                                                    "Id": "Component-2-Id",
                                                    "Name": "Component-2-Name",
                                                    "Type": "Component-2-Type"
                                                }
                                            ]
                                        },
                                        {
                                            "Id": "Tier-2-Id",
                                            "Configuration": {
                                                "Name": "Tier-2-Name",
                                                "Description": "Tier-2-Description",
                                                "Network": {
                                                    "Enabled": True
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}


@mock.patch('cot.backend.query.blueprint')
def test(blueprint_backend):

    def dummy_blueprint_backend_run(output_dir=None, **kwargs):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'blueprint.json'), 'wt+') as f:
            json.dump(BLUEPRINT_JSON, f)

    blueprint_backend.run.side_effect = dummy_blueprint_backend_run

    with tempfile.TemporaryDirectory() as temp_dir:
        os.mknod(os.path.join(temp_dir, 'root.json'))
        query.run(cwd=temp_dir)
        blueprint_backend.run.assert_called_once()
        # test that caching works
        query.run(cwd=temp_dir)
        blueprint_backend.run.assert_called_once()
        # resetting mock
        blueprint_backend.run.reset_mock()
        blueprint_backend.run.assert_not_called()
        # testing that refresh works
        query.run(cwd=temp_dir, blueprint_refresh=True)
        blueprint_backend.run.assert_called_once()
        # resetting mock
        blueprint_backend.run.reset_mock()
        blueprint_backend.run.assert_not_called()
        # testing that mock input source has unique cache
        query.run(cwd=temp_dir, blueprint_generation_input_source='mock')
        blueprint_backend.run.assert_called_once()
        blueprint_backend.run.reset_mock()
        blueprint_backend.run.assert_not_called()
        # testing that previosly created cache is used
        query.run(cwd=temp_dir)
        blueprint_backend.run.assert_not_called()
        # testing queries
        results = query.run(cwd=temp_dir, list_tiers=True, list_components=True, query="Tenants[0].Id")
        # testing the contents of the results
        assert len(results['tiers']) == 2
        assert {
            "Id": "Tier-1-Id",
            "Name": "Tier-1-Name",
            "Description": "Tier-1-Description",
            "NetworkEnabledState": False
        } in results['tiers']
        assert {
            "Id": "Tier-2-Id",
            "Name": "Tier-2-Name",
            "Description": "Tier-2-Description",
            "NetworkEnabledState": True
        }
        assert len(results['components']) == 2
        assert {
            "Id": "Component-1-Id",
            "Name": "Component-1-Name",
            "Type": "Component-1-Type"
        } in results['components']
        assert {
            "Id": "Component-2-Id",
            "Name": "Component-2-Name",
            "Type": "Component-2-Type"
        } in results['components']
        assert results['query'] == 'Tenant-Id'
