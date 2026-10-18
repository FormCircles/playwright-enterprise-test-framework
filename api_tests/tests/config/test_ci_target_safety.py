"""Regression tests for PETF-74 CI target safety."""

from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.fixture(autouse=True)
def clear_url_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent host environment variables from affecting tests."""
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("PYTEST_BASE_URL", raising=False)


def test_ci_uses_approved_yaml_target() -> None:
    settings = Settings("ci")

    assert settings.env == "ci"
    assert settings.base_url == "http://127.0.0.1:8080"


def test_ci_accepts_explicit_approved_target() -> None:
    settings = Settings(
        "ci",
        cli_overrides={"base_url": "http://127.0.0.1:8080"},
    )

    assert settings.base_url == "http://127.0.0.1:8080"


@pytest.mark.parametrize(
    "target",
    [
        "https://production.example.com",
        "https://staging.api.formcircles.com",
        "http://fastapi:8080",
        "http://localhost:8080",
        "http://127.0.0.1:9090",
    ],
)
def test_ci_rejects_unapproved_cli_target(target: str) -> None:
    with pytest.raises(ValueError, match="Unsafe CI BASE_URL"):
        Settings("ci", cli_overrides={"base_url": target})


@pytest.mark.parametrize(
    "variable",
    ["BASE_URL", "PYTEST_BASE_URL"],
)
def test_ci_rejects_unapproved_environment_target(
    variable: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(variable, "https://production.example.com")

    with pytest.raises(ValueError, match="Unsafe CI BASE_URL"):
        Settings("ci")


def test_ci_cli_precedence_remains_intact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "https://production.example.com")

    settings = Settings(
        "ci",
        cli_overrides={"base_url": "http://127.0.0.1:8080"},
    )

    assert settings.base_url == "http://127.0.0.1:8080"


def test_docker_target_remains_supported() -> None:
    settings = Settings("docker")

    assert settings.base_url == "http://fastapi:8080"


def test_staging_target_remains_supported() -> None:
    settings = Settings("staging")

    assert settings.base_url == "https://staging.api.formcircles.com"


def test_k8s_target_remains_supported() -> None:
    settings = Settings("k8s")

    assert settings.base_url == "http://fastapi-mock-app:8080"
