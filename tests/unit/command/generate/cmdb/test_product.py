import collections
from unittest import mock
from click.testing import CliRunner
from hamlet.command.generate.cmdb import generate_product
from tests.unit.command.generate.test_generate_command import run_generate_command_test

OPTIONS = collections.OrderedDict()
OPTIONS["!--product-id,product_id"] = "test-product-id"
OPTIONS["--product-name,product_name"] = ("test-product-name", "test-product-id")
OPTIONS["--dns-zone,dns_zone"] = ("test-zone-name", "")
OPTIONS["--environment-id,environment_id"] = (
    "test-environment-id",
    "test-environment-id",
)
OPTIONS["--environment-name,environment_name"] = (
    "test-environment-name",
    "test-environment-name",
)
OPTIONS["--segment-id,segment_id"] = ("test-segment-id", "default")
OPTIONS["--segment-name,segment_name"] = ("test-segment-name", "default")


@mock.patch("hamlet.command.generate.cmdb.generate_product_backend")
def test(generate_prodcut_backend):
    run_generate_command_test(
        CliRunner(), generate_product, generate_prodcut_backend.run, OPTIONS
    )
