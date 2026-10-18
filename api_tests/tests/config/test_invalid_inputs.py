"""Missing-value, invalid-input, and environment regression tests."""

from __future__ import annotations

from copy import deepcopy

import pytest

from core.config.settings import Settings


@pytest.fixture(autouse=True)
def clear_configuration_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Keep tests independent of host configuration."""
    for variable in (
        "BASE_URL",
        "PYTEST_BASE_URL",
        "TEST_USERNAME",
    ):
        monkeypatch.delenv(variable, raising=False)


@pytest.fixture
def configured_environments(
    monkeypatch: pytest.MonkeyPatch,
) -> dict:
    """Provide isolated environment configuration for each test."""
    environments = deepcopy(Settings._load_environments())

    monkeypatch.setattr(
        Settings,
        "_load_environments",
        staticmethod(lambda: environments),
    )

    return environments


@pytest.mark.parametrize(
    ("environment", "expected_url", "expected_username"),
    [
        ("local", "http://127.0.0.1:8080", "admin"),
        ("dev", "http://127.0.0.1:8080", "admin"),
        ("ci", "http://127.0.0.1:8080", "admin"),
        ("docker", "http://fastapi:8080", "admin"),
        ("k8s", "http://fastapi-mock-app:8080", "admin"),
        ("staging", "https://staging.api.formcircles.com", "automation"),
    ],
)
def test_supported_environment_defaults(
    environment: str,
    expected_url: str,
    expected_username: str,
) -> None:
    settings = Settings(environment)

    assert settings.env == environment
    assert settings.base_url == expected_url
    assert settings.username == expected_username


@pytest.mark.parametrize(
    "missing_key",
    [
        "base_url",
        "username",
    ],
)
def test_missing_required_yaml_value_is_rejected(
    configured_environments: dict,
    missing_key: str,
) -> None:
    configured_environments["local"].pop(missing_key)

    with pytest.raises(ValueError, match=missing_key):
        Settings("local")


@pytest.mark.parametrize(
    ("key", "invalid_value"),
    [
        ("base_url", None),
        ("base_url", 123),
        ("base_url", ""),
        ("base_url", "   "),
        ("username", None),
        ("username", 123),
        ("username", ""),
        ("username", "   "),
    ],
)
def test_invalid_required_yaml_values(
    configured_environments: dict,
    key: str,
    invalid_value: object,
) -> None:
    configured_environments["local"][key] = invalid_value

    with pytest.raises(ValueError, match=key):
        Settings("local")


@pytest.mark.parametrize(
    ("key", "invalid_value"),
    [
        ("request_timeout_ms", 0),
        ("request_timeout_ms", -1),
        ("request_timeout_ms", "30000"),
        ("request_timeout_ms", True),
        ("ui_timeout_ms", 0),
        ("ui_timeout_ms", -1),
        ("ui_timeout_ms", "30000"),
        ("ui_timeout_ms", True),
    ],
)
def test_invalid_timeout_configuration(
    configured_environments: dict,
    key: str,
    invalid_value: object,
) -> None:
    configured_environments["local"][key] = invalid_value

    with pytest.raises(ValueError, match=key):
        Settings("local")


@pytest.mark.parametrize(
    "invalid_value",
    [
        None,
        0,
        1,
        "true",
        "false",
        [],
    ],
)
def test_invalid_headless_configuration(
    configured_environments: dict,
    invalid_value: object,
) -> None:
    configured_environments["local"]["headless"] = invalid_value

    with pytest.raises(ValueError, match="headless"):
        Settings("local")


@pytest.mark.parametrize(
    ("variable", "invalid_url"),
    [
        ("BASE_URL", ""),
        ("BASE_URL", "not-a-url"),
        ("BASE_URL", "ftp://example.com"),
        ("BASE_URL", "http://example.com:99999"),
        ("PYTEST_BASE_URL", ""),
        ("PYTEST_BASE_URL", "not-a-url"),
        ("PYTEST_BASE_URL", "http://user:pass@example.com"),
        ("PYTEST_BASE_URL", "https://example.com?token=secret"),
    ],
)
def test_invalid_environment_url_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    variable: str,
    invalid_url: str,
) -> None:
    monkeypatch.setenv(variable, invalid_url)

    with pytest.raises(ValueError, match="base_url"):
        Settings("local")


@pytest.mark.parametrize(
    "invalid_environment",
    [
        "",
        "production",
        "LOCAL",
        "unknown",
    ],
)
def test_unknown_environment_is_rejected(
    invalid_environment: str,
) -> None:
    with pytest.raises(ValueError, match="Unknown environment"):
        Settings(invalid_environment)
