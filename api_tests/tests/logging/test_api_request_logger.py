from __future__ import annotations

import logging

from core.logging.api_request_logger import (
    APIRequestLogEntry,
    log_api_request,
)


def test_logs_request_metadata(caplog) -> None:
    caplog.set_level(logging.INFO)

    log_api_request(
        APIRequestLogEntry(
            method="GET",
            url="/api/devices",
            status=200,
            duration_ms=12.34,
        )
    )

    assert "method=GET" in caplog.text
    assert "url=/api/devices" in caplog.text
    assert "status=200" in caplog.text
    assert "duration_ms=12.34" in caplog.text


def test_does_not_log_secrets(caplog) -> None:
    caplog.set_level(logging.INFO)

    secret = "super-secret-token"

    log_api_request(
        APIRequestLogEntry(
            method="POST",
            url="/api/login",
            status=200,
            duration_ms=8.50,
        )
    )

    assert secret not in caplog.text
    assert "authorization" not in caplog.text.lower()
    assert "password" not in caplog.text.lower()