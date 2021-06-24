import os
import hashlib
import json
import tempfile
from unittest import mock
from click.testing import CliRunner
from hamlet.command.query import query_group as query


def template_backend_run_mock(data):
    def run(
        entrance='blueprint',
        output_filename='blueprint-config.json',
        output_dir=None,
        deployment_mode=None,
        generation_input_source=None,
        generation_provider=None,
        generation_framework=None,
        log_level=None,
        root_dir=None,
        tenant=None,
        account=None,
        product=None,
        environment=None,
        segment=None,
    ):
        os.makedirs(output_dir, exist_ok=True)
        blueprint_filename = os.path.join(output_dir, output_filename)
        with open(blueprint_filename, 'wt+') as f:
            json.dump(data, f)
    return run


def mock_backend(blueprint=None):
    def decorator(func):
        @mock.patch('hamlet.backend.query.context.Context')
        @mock.patch('hamlet.backend.query.template')
        def wrapper(blueprint_mock, ContextClassMock, *args, **kwargs):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(hashlib.md5(str(blueprint).encode()).hexdigest())
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(blueprint)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

        return wrapper
    return decorator


@mock_backend({
    'test': {
        'blueprint': {
            'data': 'test data'
        }
    }
})
def test_query_get(blueprint_mock, ContextClassMock):

    # when file is not found blueprint generation should be started
    blueprint_mock.run.assert_not_called()

    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'get',
            'test.blueprint.data'
        ]
    )
    print(result.exc_info)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == "test data"

    # test caching
    # caching mechanism should prevent regeneration

    result = cli.invoke(
        query,
        [
            '--use-cache',
            'get',
            'test.blueprint.data'
        ]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == "test data"

    blueprint_mock.run.assert_called_once()

    # test force refresh

    result = cli.invoke(
        query,
        [
            '--no-use-cache',
            'get',
            'test.blueprint.data'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == "test data"

    blueprint_mock.run.call_count == 2


def Tiers(tiers):
    return {
        'Tenants': [
            {
                'Products': [
                    {
                        'Environments': [
                            {
                                'Segments': [
                                    {
                                        'Tiers': tiers
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Configuration': {
                'Name': 'ConfigurationName[1]',
                'Description': 'ConfigurationDescription[1]',
                'Network': {
                    'Enabled': True
                }
            }
        },
        {
            'Id': "TierId[2]",
            'Configuration': {
                'Name': 'ConfigurationName[2]',
                'Description': 'ConfigurationDescription[2]',
                'Network': {
                    'Enabled': False
                }
            }
        }
    ]
))
def test_query_list_tiers(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'list', 'tiers',
            '--output-format', 'json'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        'Id': 'TierId[1]',
        'Name': 'ConfigurationName[1]',
        'Description': 'ConfigurationDescription[1]',
        'NetworkEnabledState': True
    } in result
    assert {
        'Id': 'TierId[2]',
        'Name': 'ConfigurationName[2]',
        'Description': 'ConfigurationDescription[2]',
        'NetworkEnabledState': False
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Name': 'ComponentName[1]',
                    'Type': 'ComponentType[1]'
                }
            ]
        },
        {
            'Id': "TierId[2]",
            'Components': [
                {
                    'Id': 'ComponentId[2]',
                    'Name': 'ComponentName[2]',
                    'Type': 'ComponentType[2]'
                },
                {
                    'Id': 'ComponentId[3]',
                    'Name': 'ComponentName[3]',
                    'Type': 'ComponentType[3]'
                }
            ]
        }
    ]
))
def test_query_list_components(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'list', 'components',
            '--output-format', 'json'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 3
    assert {
        'Id': 'ComponentId[1]',
        'Name': 'ComponentName[1]',
        'Type': 'ComponentType[1]',
        'TierId': 'TierId[1]'
    } in result
    assert {
        'Id': 'ComponentId[2]',
        'Name': 'ComponentName[2]',
        'Type': 'ComponentType[2]',
        'TierId': 'TierId[2]'
    } in result
    assert {
        'Id': 'ComponentId[3]',
        'Name': 'ComponentName[3]',
        'Type': 'ComponentType[3]',
        'TierId': 'TierId[2]'
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[1]'
                                },
                                'FullName': 'FullName[1]'
                            },
                            'Configuration': {
                                'Solution': {
                                    'Enabled': True,
                                    'DeploymentUnits': [
                                        'DeploymentUnit[1][1]',
                                        'DeploymentUnit[1][2]'
                                    ]
                                }
                            }
                        }
                    ]
                }
            ]
        },
        {
            'Id': "TierId[2]",
            'Components': [
                {
                    'Id': 'ComponentId[2]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[2]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[2]'
                                },
                                'FullName': 'FullName[2]'
                            },
                            'Configuration': {
                                'Solution': {
                                    'Enabled': False,
                                    'DeploymentUnits': [
                                        'DeploymentUnit[2][1]'
                                    ]
                                }
                            }
                        }
                    ]
                },
                {
                    'Id': 'ComponentId[3]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[3]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[3]'
                                },
                                'FullName': 'FullName[3]'
                            },
                            'Configuration': {
                                'Solution': {
                                    'Enabled': False,
                                    'DeploymentUnits': [
                                        'DeploymentUnit[3][1]',
                                        'DeploymentUnit[3][2]'
                                    ]
                                }
                            }
                        },
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[4]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[4]'
                                },
                                'FullName': 'FullName[4]'
                            },
                            'Configuration': {
                                'Solution': {
                                    'Enabled': True,
                                    'DeploymentUnits': [
                                        'DeploymentUnit[4][1]'
                                    ]
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_list_occurrences(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'list', 'occurrences',
            '-t', 'TierId[2]',
            '-c', 'ComponentId[3]',
            '--output-format', 'json'
        ]
    )
    print(result.exception)
    assert result.exit_code == 0
    result = json.loads(result.output)
    assert len(result) == 2
    assert {
        'InstanceId': 'InstanceRawId[4]',
        'VersionId': 'VersionRawId[4]',
        'FullName': 'FullName[4]',
        'DeploymentUnits': ['DeploymentUnit[4][1]'],
        'Enabled': True
    } in result
    assert {
        'InstanceId': 'InstanceRawId[3]',
        'VersionId': 'VersionRawId[3]',
        'FullName': 'FullName[3]',
        'DeploymentUnits': ['DeploymentUnit[3][1]', 'DeploymentUnit[3][2]'],
        'Enabled': False
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawIdd': 'VersionRawId[1]'
                                }
                            }
                        }
                    ]
                }
            ]
        },
        {
            'Id': "TierId[2]",
            'Components': [
                {
                    'Id': 'ComponentId[2]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[2]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[2]'
                                }
                            }
                        },
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[3]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[3]'
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_describe_occurence(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'describe', 'occurrence',
            '-t', 'TierId[2]',
            '-c', 'ComponentId[2]',
            '-i', 'InstanceRawId[2]',
            '-v', 'VersionRawId[2]'
        ]
    )
    print(result.exc_info)
    result = json.loads(result.output)
    assert len(result) == 1
    assert {
        "Core": {
            "Instance": {
                "RawId": "InstanceRawId[2]"
            },
            "Version": {
                "RawId": "VersionRawId[2]"
            }
        }
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[1]'
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_describe_occurence_get(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'describe', 'occurrence',
            '-t', 'TierId[1]',
            '-c', 'ComponentId[1]',
            '-i', 'InstanceRawId[1]',
            '-v', 'VersionRawId[1]',
            'get',
            '[*].Core.Instance.RawId'
        ]
    )
    print(result.output)
    result = json.loads(result.output)
    assert len(result) == 1
    assert "InstanceRawId[1]" in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[1]'
                                }
                            },
                            'State': {
                                'ResourceGroups': {
                                    'AttributesContainer[1]': {
                                        'Attributes': [
                                            {
                                                'Attribute[1]': 'Value[1]',
                                                'Attribute[2]': 'Value[2]'
                                            }
                                        ]
                                    },
                                    'AttributesContainer[2]': {
                                        'Attributes': [
                                            {
                                                'Attribute[3]': 'Value[3]',
                                                'Attribute[4]': 'Value[4]',
                                                'Attribute[5]': 5
                                            }
                                        ]
                                    },
                                    'Attributes': [
                                        {
                                            'Attribute[6]': 'Value[6]'
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_describe_occurence_attributes(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'describe', 'occurrence',
            '-t', 'TierId[1]',
            '-c', 'ComponentId[1]',
            '-i', 'InstanceRawId[1]',
            '-v', 'VersionRawId[1]',
            'attributes',
            '--output-format', 'json'
        ]
    )
    print(result.exception)
    result = json.loads(result.output)
    assert len(result) == 5
    assert {
        'Key': 'Attribute[1]',
        'Value': 'Value[1]'
    } in result
    assert {
        'Key': 'Attribute[2]',
        'Value': 'Value[2]'
    } in result
    assert {
        'Key': 'Attribute[3]',
        'Value': 'Value[3]'
    } in result
    assert {
        'Key': 'Attribute[4]',
        'Value': 'Value[4]'
    } in result
    assert {
        'Key': 'Attribute[5]',
        'Value': 5
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[1]'
                                }
                            },
                            'Configuration': {
                                'Solution': {
                                    'Param[1]': 'Value[1]',
                                    'Param[2]': 'Value[2]'
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_describe_occurence_solution(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'describe', 'occurrence',
            '-t', 'TierId[1]',
            '-c', 'ComponentId[1]',
            '-i', 'InstanceRawId[1]',
            '-v', 'VersionRawId[1]',
            'solution'
        ]
    )
    print(result.exception)
    result = json.loads(result.output)
    assert len(result) == 1
    assert {
        'Param[1]': 'Value[1]',
        'Param[2]': 'Value[2]'
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[1]'
                                }
                            },
                            'Configuration': {
                                'Settings': {
                                    'Param[1]': 'Value[1]',
                                    'Param[2]': 'Value[2]'
                                }
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_describe_occurence_settings(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'describe', 'occurrence',
            '-t', 'TierId[1]',
            '-c', 'ComponentId[1]',
            '-i', 'InstanceRawId[1]',
            '-v', 'VersionRawId[1]',
            'settings'
        ]
    )
    print(result.exception)
    result = json.loads(result.output)
    assert len(result) == 1
    assert {
        'Param[1]': 'Value[1]',
        'Param[2]': 'Value[2]'
    } in result


@mock_backend(Tiers(
    [
        {
            'Id': "TierId[1]",
            'Components': [
                {
                    'Id': 'ComponentId[1]',
                    'Occurrences': [
                        {
                            'Core': {
                                'Instance': {
                                    'RawId': 'InstanceRawId[1]'
                                },
                                'Version': {
                                    'RawId': 'VersionRawId[1]'
                                }
                            },
                            'State': {
                                'Resources': [
                                    'Resource[1]',
                                    'Resource[2]'
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    ]
))
def test_query_describe_occurence_resources(blueprint_mock, ContextClassMock):
    cli = CliRunner()
    result = cli.invoke(
        query,
        [
            'describe', 'occurrence',
            '-t', 'TierId[1]',
            '-c', 'ComponentId[1]',
            '-i', 'InstanceRawId[1]',
            '-v', 'VersionRawId[1]',
            'resources'
        ]
    )
    print(result.exception)
    result = json.loads(result.output)
    assert len(result) == 1
    assert [
        'Resource[1]',
        'Resource[2]'
    ] in result
