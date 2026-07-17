from __future__ import annotations

import logging
from dataclasses import dataclass


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class APIRequestLogEntry:
    """Safe metadata describing one completed API request."""

    method: str
    url: str
    status: int
    duration_ms: float


def log_api_request(entry: APIRequestLogEntry) -> None:
    """Log non-sensitive API request metadata."""

    LOGGER.info(
        "API request completed "
        "method=%s url=%s status=%s duration_ms=%.2f",
        entry.method,
        entry.url,
        entry.status,
        entry.duration_ms,
    )