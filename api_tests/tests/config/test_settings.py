from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.mark.parametrize(
    "environment",
    [
        "local",
        "ci",
    ],
)
def test_loads_local_and_ci_defaults(environment: str) -> None:
    settings = Settings(environment)

    assert settings.env == environment
    assert settings.base_url
    assert settings.username
    assert settings.request_timeout_ms == 30_000
    assert settings.ui_timeout_ms == 30_000
    assert settings.headless is True


def test_reads_password_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TEST_PASSWORD", "secret-value")

    settings = Settings("local")

    assert settings.password == "secret-value"


def test_does_not_store_default_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TEST_PASSWORD", raising=False)

    settings = Settings("local")

    assert settings.password == ""


def test_requires_password_for_authenticated_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TEST_PASSWORD", raising=False)

    settings = Settings("local")

    with pytest.raises(
        RuntimeError,
        match="TEST_PASSWORD is required",
    ):
        settings.require_password()


def test_environment_variables_override_yaml(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("BASE_URL", "http://override:9999")
    monkeypatch.setenv("TEST_USERNAME", "override-user")

    settings = Settings("local")

    assert settings.base_url == "http://override:9999"
    assert settings.username == "override-user"


def test_rejects_unknown_environment() -> None:
    with pytest.raises(ValueError, match="Unknown environment"):
        Settings("unsupported")
