from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


REDACTED = "***REDACTED***"

SENSITIVE_KEYS = {
    "authorization",
    "proxy-authorization",
    "password",
    "passwd",
    "secret",
    "client-secret",
    "client_secret",
    "access-token",
    "access_token",
    "refresh-token",
    "refresh_token",
    "id-token",
    "id_token",
    "api-key",
    "api_key",
    "apikey",
    "x-api-key",
    "cookie",
    "set-cookie",
}

BEARER_TOKEN_PATTERN = re.compile(
    r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+"
)


def normalize_sensitive_key(key: object) -> str:
    """Normalize a key for case-insensitive secret detection."""

    return str(key).strip().lower()


def is_sensitive_key(key: object) -> bool:
    """Return whether a mapping or header key is sensitive."""

    return normalize_sensitive_key(key) in SENSITIVE_KEYS


def sanitize_text(value: str) -> str:
    """Mask bearer tokens embedded in arbitrary text."""

    return BEARER_TOKEN_PATTERN.sub(
        f"Bearer {REDACTED}",
        value,
    )


def sanitize_url(url: str) -> str:
    """Mask sensitive query-string values in a URL."""

    parsed = urlsplit(url)

    if not parsed.query:
        return sanitize_text(url)

    sanitized_query = []

    for key, value in parse_qsl(
        parsed.query,
        keep_blank_values=True,
    ):
        if is_sensitive_key(key):
            sanitized_query.append((key, REDACTED))
        else:
            sanitized_query.append(
                (key, sanitize_text(value))
            )

    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(sanitized_query),
            parsed.fragment,
        )
    )


def sanitize_mapping(
    values: Mapping[object, Any],
) -> dict[object, Any]:
    """Return a sanitized copy of a mapping."""

    sanitized: dict[object, Any] = {}

    for key, value in values.items():
        if is_sensitive_key(key):
            sanitized[key] = REDACTED
        else:
            sanitized[key] = sanitize_value(value)

    return sanitized


def sanitize_value(value: Any) -> Any:
    """Recursively sanitize common loggable data structures."""

    if isinstance(value, Mapping):
        return sanitize_mapping(value)

    if isinstance(value, str):
        return sanitize_text(value)

    if isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        return [sanitize_value(item) for item in value]

    return value