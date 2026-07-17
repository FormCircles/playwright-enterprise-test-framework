from __future__ import annotations

import logging
from dataclasses import dataclass

from core.logging.sanitization import sanitize_url


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class APIRequestLogEntry:
    """Safe metadata describing one completed API request."""

    method: str
    url: str
    status: int
    duration_ms: float


def log_api_request(entry: APIRequestLogEntry) -> None:
    """Log sanitized API request metadata."""

    LOGGER.info(
        "API request completed "
        "method=%s url=%s status=%s duration_ms=%.2f",
        entry.method.upper(),
        sanitize_url(entry.url),
        entry.status,
        entry.duration_ms,
    )