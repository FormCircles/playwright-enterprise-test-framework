from __future__ import annotations

from core.logging.sanitization import (
    REDACTED,
    sanitize_mapping,
    sanitize_text,
    sanitize_url,
    sanitize_value,
)


def test_masks_authorization_header() -> None:
    headers = {
        "Authorization": "Bearer very-secret-token",
        "Content-Type": "application/json",
    }

    sanitized = sanitize_mapping(headers)

    assert sanitized["Authorization"] == REDACTED
    assert sanitized["Content-Type"] == "application/json"
    assert "very-secret-token" not in str(sanitized)


def test_masks_sensitive_headers_case_insensitively() -> None:
    headers = {
        "authorization": "Bearer secret-one",
        "X-API-KEY": "secret-two",
        "Cookie": "session=secret-three",
        "set-cookie": "session=secret-four",
    }

    sanitized = sanitize_mapping(headers)

    assert sanitized["authorization"] == REDACTED
    assert sanitized["X-API-KEY"] == REDACTED
    assert sanitized["Cookie"] == REDACTED
    assert sanitized["set-cookie"] == REDACTED


def test_masks_nested_secret_values() -> None:
    payload = {
        "username": "admin",
        "credentials": {
            "password": "password-value",
            "access_token": "token-value",
        },
    }

    sanitized = sanitize_value(payload)

    assert sanitized["username"] == "admin"
    assert sanitized["credentials"]["password"] == REDACTED
    assert sanitized["credentials"]["access_token"] == REDACTED

    rendered = str(sanitized)

    assert "password-value" not in rendered
    assert "token-value" not in rendered


def test_masks_bearer_token_in_text() -> None:
    value = "Request failed with Bearer abc.def.ghi"

    sanitized = sanitize_text(value)

    assert sanitized == f"Request failed with Bearer {REDACTED}"
    assert "abc.def.ghi" not in sanitized


def test_masks_sensitive_url_query_parameters() -> None:
    url = (
        "/api/devices?"
        "access_token=secret-token&"
        "page=2&"
        "api_key=secret-api-key"
    )

    sanitized = sanitize_url(url)

    assert "secret-token" not in sanitized
    assert "secret-api-key" not in sanitized
    assert "page=2" in sanitized
    assert "access_token=" in sanitized
    assert "api_key=" in sanitized


def test_does_not_modify_original_mapping() -> None:
    original = {
        "Authorization": "Bearer original-token",
        "nested": {
            "password": "original-password",
        },
    }

    sanitize_mapping(original)

    assert original["Authorization"] == "Bearer original-token"
    assert original["nested"]["password"] == "original-password"


def test_preserves_non_sensitive_values() -> None:
    value = {
        "status": "healthy",
        "device_id": 42,
        "enabled": True,
    }

    assert sanitize_value(value) == value