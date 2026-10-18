"""Tests for PETF-73 explicit pytest CLI override detection."""

from types import SimpleNamespace

import pytest

from core.config.pytest_options import explicit_base_url


def make_config(args, resolved_url):
    return SimpleNamespace(
        invocation_params=SimpleNamespace(args=tuple(args)),
        getoption=lambda option: resolved_url,
    )


def test_no_explicit_option(monkeypatch):
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)

    config = make_config([], "http://plugin:8080")

    assert explicit_base_url(config) is None


def test_direct_cli_option(monkeypatch):
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)

    config = make_config(
        ["--base-url=http://cli:8080"],
        "http://cli:8080",
    )

    assert explicit_base_url(config) == "http://cli:8080"


def test_space_separated_cli_option(monkeypatch):
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)

    config = make_config(
        ["--base-url", "http://cli:8080"],
        "http://cli:8080",
    )

    assert explicit_base_url(config) == "http://cli:8080"


def test_pytest_addopts_option(monkeypatch):
    monkeypatch.setenv(
        "PYTEST_ADDOPTS",
        "--base-url=http://cli:8080",
    )

    config = make_config([], "http://cli:8080")

    assert explicit_base_url(config) == "http://cli:8080"


def test_direct_cli_overrides_pytest_addopts(monkeypatch):
    monkeypatch.setenv(
        "PYTEST_ADDOPTS",
        "--base-url=http://addopts:8080",
    )

    config = make_config(
        ["--base-url=http://cli:8080"],
        "http://cli:8080",
    )

    assert explicit_base_url(config) == "http://cli:8080"


def test_duplicate_options_use_pytest_resolved_value(monkeypatch):
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)

    config = make_config(
        [
            "--base-url=http://first:8080",
            "--base-url=http://second:8080",
        ],
        "http://second:8080",
    )

    assert explicit_base_url(config) == "http://second:8080"


def test_missing_cli_value_is_rejected(monkeypatch):
    monkeypatch.delenv("PYTEST_ADDOPTS", raising=False)

    config = make_config(["--base-url"], None)

    with pytest.raises(ValueError, match="requires a value"):
        explicit_base_url(config)
