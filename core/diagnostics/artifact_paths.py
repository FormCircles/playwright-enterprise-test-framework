"""Canonical run, worker, suite, and test artifact directory contract."""

from __future__ import annotations

import hashlib
from pathlib import Path

from core.diagnostics.screenshot_paths import sanitize_component
from core.diagnostics.trace_paths import reserve_trace_directory

ARTIFACT_ROOT = Path("artifacts")

ARTIFACT_KINDS = frozenset(
    {
        "logs",
        "screenshots",
        "traces",
        "attachments",
    }
)


def _test_component(node_id: str) -> str:
    """Return an opaque, stable component for a complete pytest node ID."""
    if not node_id:
        raise ValueError("node_id must not be empty")

    return hashlib.sha256(node_id.encode("utf-8")).hexdigest()[:16]


def run_artifact_directory(
    *,
    run_id: str,
    root: Path = ARTIFACT_ROOT,
) -> Path:
    """Return the canonical directory for one execution."""
    return root / sanitize_component(run_id)


def report_artifact_directory(
    *,
    run_id: str,
    root: Path = ARTIFACT_ROOT,
) -> Path:
    """Return the shared report directory for one execution."""
    return run_artifact_directory(run_id=run_id, root=root) / "reports"


def metadata_artifact_directory(
    *,
    run_id: str,
    root: Path = ARTIFACT_ROOT,
) -> Path:
    """Return the run metadata directory."""
    return run_artifact_directory(run_id=run_id, root=root) / "metadata"


def worker_artifact_directory(
    *,
    run_id: str,
    worker_id: str,
    root: Path = ARTIFACT_ROOT,
) -> Path:
    """Return the directory owned by one worker."""
    return (
        run_artifact_directory(run_id=run_id, root=root)
        / "workers"
        / sanitize_component(worker_id)
    )


def case_artifact_directory(
    *,
    run_id: str,
    worker_id: str,
    suite_id: str,
    node_id: str,
    root: Path = ARTIFACT_ROOT,
) -> Path:
    """Return the deterministic base directory for one pytest test."""
    return (
        worker_artifact_directory(
            run_id=run_id,
            worker_id=worker_id,
            root=root,
        )
        / sanitize_component(suite_id)
        / _test_component(node_id)
    )


def artifact_kind_directory(
    *,
    run_id: str,
    worker_id: str,
    suite_id: str,
    node_id: str,
    kind: str,
    root: Path = ARTIFACT_ROOT,
) -> Path:
    """Return the canonical directory for a supported artifact kind."""
    if kind not in ARTIFACT_KINDS:
        raise ValueError(f"Unsupported artifact kind: {kind}")

    return (
        case_artifact_directory(
            run_id=run_id,
            worker_id=worker_id,
            suite_id=suite_id,
            node_id=node_id,
            root=root,
        )
        / kind
    )


def ensure_artifact_directory(path: Path) -> Path:
    """Create a directory safely; repeated calls return the same path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def reserve_artifact_directory(path: Path) -> Path:
    """Atomically reserve a new directory without replacing prior evidence."""
    return reserve_trace_directory(path)
