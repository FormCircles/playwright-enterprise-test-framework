from __future__ import annotations

import pytest

from core.environment import (
    assert_reset_allowed,
    is_reset_allowed,
)


@pytest.mark.parametrize(
    "environment",
    [
        "dev",
        "local",
        "ci",
        "test",
        "staging",
    ],
)
def test_reset_is_allowed_in_non_production(environment):
    assert is_reset_allowed(environment) is True


@pytest.mark.parametrize(
    "environment",
    [
        "prod",
        "production",
        "PROD",
        " Production ",
    ],
)
def test_reset_is_blocked_in_production(environment):
    assert is_reset_allowed(environment) is False


def test_reset_guard_raises_in_production():
    with pytest.raises(RuntimeError) as error:
        assert_reset_allowed("production")

    assert "forbidden" in str(error.value)