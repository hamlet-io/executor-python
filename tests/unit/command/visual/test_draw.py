import collections
import tempfile
import hashlib
import json
import os

from unittest import mock
from click.testing import CliRunner
from hamlet.command.visual import draw_diagrams as draw_diagrams
from tests.unit.command.test_option_generation import (
    run_options_test,
    run_validatable_option_test,
)


ALL_VALID_OPTIONS = collections.OrderedDict()

ALL_VALID_OPTIONS["!-i,--diagram-id"] = ["Diagram1"]
ALL_VALID_OPTIONS["!-d,--asset-dir"] = "./"
ALL_VALID_OPTIONS["-s,--src-dir"] = "./"


def template_backend_run_mock(data):
    def run(
        entrance="diagraminfo",
        output_filename="diagraminfo.json",
        deployment_mode=None,
        output_dir=None,
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
        unitlist_filename = os.path.join(output_dir, output_filename)
        with open(unitlist_filename, "wt+") as f:
            json.dump(data, f)

    return run


def mock_backend(unitlist=None):
    def decorator(func):
        @mock.patch("hamlet.command.visual.create_diagram_backend")
        @mock.patch("hamlet.command.visual.create_template_backend")
        @mock.patch("hamlet.backend.query.context.Context")
        @mock.patch("hamlet.backend.query.template")
        def wrapper(
            blueprint_mock,
            ContextClassMock,
            create_template_backend,
            create_diagram_backend,
            *args,
            **kwargs
        ):
            with tempfile.TemporaryDirectory() as temp_cache_dir:

                ContextObjectMock = ContextClassMock()
                ContextObjectMock.md5_hash.return_value = str(
                    hashlib.md5(str(unitlist).encode()).hexdigest()
                )
                ContextObjectMock.cache_dir = temp_cache_dir

                blueprint_mock.run.side_effect = template_backend_run_mock(unitlist)

                return func(blueprint_mock, ContextClassMock, *args, **kwargs)

        return wrapper

    return decorator


diagram_list = {
    "Diagrams": [
        {
            "Id": "Diagram1",
        }
    ]
}


@mock_backend(diagram_list)
def test_input_valid(create_template_backend, create_diagram_backend):
    run_options_test(
        CliRunner(), draw_diagrams, ALL_VALID_OPTIONS, create_template_backend.run
    )


@mock_backend(diagram_list)
def test_input_validation(create_template_backend, create_diagram_backend):
    runner = CliRunner()
    run_validatable_option_test(
        runner,
        draw_diagrams,
        create_template_backend.run,
        {"-i": "overview", "-d": "./"},
        [],
    )
