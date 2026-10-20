"""Tests for PETF trace activation policy."""

import pytest

from core.config.trace_policy import resolve_trace_mode


@pytest.mark.parametrize(
    ("mode", "expected"),
    [
        ("off", "off"),
        ("on-failure", "retain-on-failure"),
    ],
)
def test_supported_trace_modes(mode, expected):
    assert resolve_trace_mode(mode) == expected


@pytest.mark.parametrize(
    "mode",
    ["on", "on-retry", "on-failure-or-retry", "invalid", ""],
)
def test_unsupported_trace_modes(mode):
    with pytest.raises(ValueError):
        resolve_trace_mode(mode)
