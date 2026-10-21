"""Collision-safe native Playwright artifact directories."""

from __future__ import annotations

import hashlib
from pathlib import Path

from core.diagnostics.screenshot_paths import sanitize_component


def trace_artifact_directory(
    *, output_directory: Path, run_id: str, worker_id: str, node_id: str
) -> Path:
    """Return a deterministic base directory; reservation handles repeated tests."""
    digest = hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:16]
    return (
        output_directory
        / sanitize_component(run_id)
        / sanitize_component(worker_id)
        / digest
    )


def reserve_trace_directory(base: Path) -> Path:
    """Atomically reserve a distinct directory; never overwrite earlier evidence."""
    base.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(10000):
        candidate = base if attempt == 0 else base.with_name(f"{base.name}-{attempt}")
        try:
            candidate.mkdir(exist_ok=False)
        except FileExistsError:
            continue
        return candidate
    raise RuntimeError(f"Too many artifact directory collisions for {base}")
