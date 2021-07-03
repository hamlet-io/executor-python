import pytest
from hamlet.backend.create.template import utils


def test_semver():
    assert utils.semver_valid("v1.0.0") == ("1", "0", "0", None, None)
    assert utils.semver_valid("v2.0.1") == ("2", "0", "1", None, None)
    assert utils.semver_valid("2.0.1-a+b") == ("2", "0", "1", "a", "b")
    assert utils.semver_valid("2.0.1+b") == ("2", "0", "1", None, "b")
    assert utils.semver_valid("2.0.1-a") == ("2", "0", "1", "a", None)
    with pytest.raises(ValueError):
        utils.semver_valid("1.0")
    assert utils.semver_compare("1.0.0", "1.0.1") < 0
    assert utils.semver_compare("1.0.1", "1.0.0") > 0
    assert utils.semver_compare("1.0.0", "1.0.0") == 0

    assert utils.semver_clean("v1.2.3") == "1.2.3"
    assert utils.semver_clean("v1.X.x") == "1.0.0"

    assert utils.semver_satisfies("1.0.0", ["<=1.0.0"])
    assert utils.semver_satisfies("1.0.0", [">=1.0.0"])
    assert utils.semver_satisfies("1.0.0", ["<=2.0.0"])
    assert utils.semver_satisfies("1.0.0", [">=0.0.1"])
    assert utils.semver_satisfies("1.0.0", ["=1.0.0"])
    assert utils.semver_satisfies("1.0.0", ["<2.0.0"])
    assert utils.semver_satisfies("1.0.0", [">0.0.1"])

    assert not utils.semver_satisfies("2.0.0", ["<=1.0.0"])
    assert not utils.semver_satisfies("0.0.1", [">=1.0.0"])
    assert not utils.semver_satisfies("1.0.1", ["=1.0.0"])
    assert not utils.semver_satisfies("3.0.0", ["<2.0.0"])
    assert not utils.semver_satisfies("1.0.0", [">2.0.0"])
