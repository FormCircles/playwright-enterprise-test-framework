"""Regression matrix for PETF configuration precedence."""

from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.mark.parametrize(
    ("cli_url", "base_url_env", "plugin_url_env", "expected"),
    [
        (
            "http://cli:8080",
            "http://environment:8080",
            "http://plugin:8080",
            "http://cli:8080",
        ),
        (
            None,
            "http://environment:8080",
            "http://plugin:8080",
            "http://environment:8080",
        ),
        (
            None,
            None,
            "http://plugin:8080",
            "http://plugin:8080",
        ),
        (
            None,
            None,
            None,
            "http://127.0.0.1:8080",
        ),
    ],
)
def test_base_url_precedence_matrix(
    monkeypatch: pytest.MonkeyPatch,
    cli_url: str | None,
    base_url_env: str | None,
    plugin_url_env: str | None,
    expected: str,
) -> None:
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("PYTEST_BASE_URL", raising=False)

    if base_url_env is not None:
        monkeypatch.setenv("BASE_URL", base_url_env)

    if plugin_url_env is not None:
        monkeypatch.setenv("PYTEST_BASE_URL", plugin_url_env)

    overrides = {"base_url": cli_url} if cli_url is not None else None

    settings = Settings("local", cli_overrides=overrides)

    assert settings.base_url == expected
