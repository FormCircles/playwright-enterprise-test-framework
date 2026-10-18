"""Tests for deterministic PETF configuration precedence."""

from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.fixture(autouse=True)
def clear_base_url_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep precedence tests independent of the host environment."""
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("PYTEST_BASE_URL", raising=False)


def test_cli_overrides_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "http://environment:8080")
    monkeypatch.setenv("PYTEST_BASE_URL", "http://plugin:8080")

    settings = Settings(
        "local",
        cli_overrides={"base_url": "http://cli:8080"},
    )

    assert settings.base_url == "http://cli:8080"


def test_base_url_environment_variable_overrides_plugin_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "http://environment:8080")
    monkeypatch.setenv("PYTEST_BASE_URL", "http://plugin:8080")

    settings = Settings("local")

    assert settings.base_url == "http://environment:8080"


def test_plugin_environment_variable_overrides_yaml(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PYTEST_BASE_URL", "http://plugin:8080")

    settings = Settings("local")

    assert settings.base_url == "http://plugin:8080"


def test_yaml_used_without_overrides() -> None:
    settings = Settings("local")

    assert settings.base_url == "http://127.0.0.1:8080"


def test_docker_environment_configuration() -> None:
    settings = Settings("docker")

    assert settings.base_url == "http://fastapi:8080"


def test_empty_cli_value_fails_instead_of_falling_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "http://environment:8080")

    with pytest.raises(ValueError, match="base_url"):
        Settings(
            "local",
            cli_overrides={"base_url": ""},
        )


def test_empty_environment_value_fails_instead_of_falling_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "")

    with pytest.raises(ValueError, match="base_url"):
        Settings("local")


def test_cli_username_overrides_environment_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TEST_USERNAME", "environment-user")

    settings = Settings(
        "local",
        cli_overrides={"username": "cli-user"},
    )

    assert settings.username == "cli-user"


def test_environment_username_overrides_yaml(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TEST_USERNAME", "environment-user")

    settings = Settings("local")

    assert settings.username == "environment-user"


def test_unknown_environment_remains_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown environment"):
        Settings(
            "production",
            cli_overrides={"base_url": "http://cli:8080"},
        )


@pytest.mark.parametrize(
    "invalid_url",
    [
        "",
        "not-a-url",
        "ftp://example.com",
        "http://",
        "http://example.com:invalid",
        "http://example.com:99999",
        "http://user:password@example.com",
        "https://example.com?token=secret",
        "https://example.com#fragment",
        "http://example.com/path with spaces",
    ],
)
def test_invalid_cli_base_url_fails_without_fallback(
    invalid_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "http://environment:8080")

    with pytest.raises(ValueError, match="base_url"):
        Settings(
            "local",
            cli_overrides={"base_url": invalid_url},
        )


@pytest.mark.parametrize(
    "valid_url",
    [
        "http://127.0.0.1:8080",
        "http://fastapi:8080",
        "http://fastapi-mock-app:8080",
        "https://staging.api.formcircles.com",
    ],
)
def test_valid_base_urls_are_accepted(valid_url: str) -> None:
    settings = Settings(
        "local",
        cli_overrides={"base_url": valid_url},
    )

    assert settings.base_url == valid_url
