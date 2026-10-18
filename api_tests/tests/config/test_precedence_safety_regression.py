"""Regression tests for configuration precedence and CI safety."""

from __future__ import annotations

import pytest

from core.config.settings import Settings


@pytest.fixture(autouse=True)
def clear_configuration_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for variable in (
        "BASE_URL",
        "PYTEST_BASE_URL",
        "TEST_USERNAME",
    ):
        monkeypatch.delenv(variable, raising=False)


@pytest.mark.parametrize(
    ("source", "invalid_url"),
    [
        ("cli", ""),
        ("cli", "ftp://example.com"),
        ("base_url", ""),
        ("base_url", "not-a-url"),
        ("plugin", ""),
        ("plugin", "http://example.com:99999"),
    ],
)
def test_invalid_higher_priority_url_never_falls_back(
    monkeypatch: pytest.MonkeyPatch,
    source: str,
    invalid_url: str,
) -> None:
    overrides = None

    if source == "cli":
        monkeypatch.setenv("BASE_URL", "http://valid:8080")
        overrides = {"base_url": invalid_url}
    elif source == "base_url":
        monkeypatch.setenv("BASE_URL", invalid_url)
        monkeypatch.setenv("PYTEST_BASE_URL", "http://valid:8080")
    else:
        monkeypatch.setenv("PYTEST_BASE_URL", invalid_url)

    with pytest.raises(ValueError, match="base_url"):
        Settings("local", cli_overrides=overrides)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("cli", "http://cli:8080"),
        ("base_url", "http://environment:8080"),
    ],
)
def test_valid_higher_priority_url_ignores_invalid_lower_priority(
    monkeypatch: pytest.MonkeyPatch,
    source: str,
    expected: str,
) -> None:
    monkeypatch.setenv("PYTEST_BASE_URL", "not-a-url")

    if source == "cli":
        monkeypatch.setenv("BASE_URL", "also-invalid")
        overrides = {"base_url": expected}
    else:
        monkeypatch.setenv("BASE_URL", expected)
        overrides = None

    settings = Settings("local", cli_overrides=overrides)

    assert settings.base_url == expected


@pytest.mark.parametrize(
    "source",
    [
        "cli",
        "base_url",
        "plugin",
    ],
)
def test_ci_rejects_unsafe_target_from_each_source(
    monkeypatch: pytest.MonkeyPatch,
    source: str,
) -> None:
    unsafe_url = "https://production.example.com"
    overrides = None

    if source == "cli":
        overrides = {"base_url": unsafe_url}
    elif source == "base_url":
        monkeypatch.setenv("BASE_URL", unsafe_url)
    else:
        monkeypatch.setenv("PYTEST_BASE_URL", unsafe_url)

    with pytest.raises(ValueError, match="Unsafe CI BASE_URL"):
        Settings("ci", cli_overrides=overrides)


@pytest.mark.parametrize(
    "source",
    [
        "cli",
        "base_url",
        "plugin",
        "yaml",
    ],
)
def test_ci_accepts_approved_target_from_each_source(
    monkeypatch: pytest.MonkeyPatch,
    source: str,
) -> None:
    approved_url = "http://127.0.0.1:8080"
    overrides = None

    if source == "cli":
        overrides = {"base_url": approved_url}
    elif source == "base_url":
        monkeypatch.setenv("BASE_URL", approved_url)
    elif source == "plugin":
        monkeypatch.setenv("PYTEST_BASE_URL", approved_url)

    settings = Settings("ci", cli_overrides=overrides)

    assert settings.base_url == approved_url


@pytest.mark.parametrize(
    "invalid_username",
    [
        "",
        "   ",
    ],
)
def test_invalid_cli_username_does_not_fall_back(
    monkeypatch: pytest.MonkeyPatch,
    invalid_username: str,
) -> None:
    monkeypatch.setenv("TEST_USERNAME", "valid-user")

    with pytest.raises(ValueError, match="username"):
        Settings(
            "local",
            cli_overrides={"username": invalid_username},
        )


@pytest.mark.parametrize(
    "invalid_username",
    [
        "",
        "   ",
    ],
)
def test_invalid_environment_username_does_not_fall_back(
    monkeypatch: pytest.MonkeyPatch,
    invalid_username: str,
) -> None:
    monkeypatch.setenv("TEST_USERNAME", invalid_username)

    with pytest.raises(ValueError, match="username"):
        Settings("local")


def test_valid_cli_username_overrides_invalid_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TEST_USERNAME", "")

    settings = Settings(
        "local",
        cli_overrides={"username": "cli-user"},
    )

    assert settings.username == "cli-user"


def test_ci_approved_cli_target_overrides_unsafe_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "BASE_URL",
        "https://production.example.com",
    )

    settings = Settings(
        "ci",
        cli_overrides={"base_url": "http://127.0.0.1:8080"},
    )

    assert settings.base_url == "http://127.0.0.1:8080"


def test_ci_unsafe_cli_target_overrides_approved_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "BASE_URL",
        "http://127.0.0.1:8080",
    )

    with pytest.raises(ValueError, match="Unsafe CI BASE_URL"):
        Settings(
            "ci",
            cli_overrides={
                "base_url": "https://production.example.com",
            },
        )
