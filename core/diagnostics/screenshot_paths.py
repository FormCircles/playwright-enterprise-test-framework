"""Deterministic, sanitized screenshot artifact paths."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def sanitize_component(value: str, *, max_length: int = 80) -> str:
    """Convert untrusted identifiers into collision-resistant path components."""
    if max_length < 14:
        raise ValueError("max_length must be at least 14")

    sanitized = re.sub(r"[^A-Za-z0-9_-]+", "_", value)
    sanitized = sanitized.strip("_-") or "unknown"

    if sanitized != value or len(sanitized) > max_length:
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
        sanitized = f"{sanitized[: max_length - 13]}-{digest}"

    return sanitized


def screenshot_artifact_path(
    *,
    output_directory: Path,
    run_id: str,
    worker_id: str,
    node_id: str,
) -> Path:
    """Build a stable screenshot path for one test and worker."""
    run_component = sanitize_component(run_id)
    worker_component = sanitize_component(worker_id)

    test_name = node_id.rsplit("::", 1)[-1]
    test_component = sanitize_component(test_name, max_length=64)

    digest = hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:16]

    return (
        output_directory
        / run_component
        / worker_component
        / f"{test_component}-{digest}.png"
    )
