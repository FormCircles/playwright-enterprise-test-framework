"""Integration checks for PETF trace configuration."""

from __future__ import annotations

import pytest

from core.config.trace_policy import resolve_trace_mode


@pytest.mark.parametrize(
    ("petf_mode", "expected"),
    [
        ("off", "off"),
        ("on-failure", "retain-on-failure"),
    ],
)
def test_petf_trace_mapping(petf_mode, expected):
    assert resolve_trace_mode(petf_mode) == expected


def test_default_trace_policy_is_off():
    assert resolve_trace_mode("off") == "off"


def test_retry_trace_policy_is_not_yet_supported():
    with pytest.raises(ValueError):
        resolve_trace_mode("on-retry")
