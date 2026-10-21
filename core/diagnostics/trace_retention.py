"""Final-outcome trace retention for PETF-managed Playwright artifacts."""

from __future__ import annotations

from pathlib import Path


def discard_successful_trace(*, artifact_directory: Path, failed: bool) -> None:
    """Remove only native trace ZIPs on success; leave video/screenshots untouched."""
    if failed or not artifact_directory.is_dir():
        return
    for trace in artifact_directory.glob("trace*.zip"):
        if trace.is_file():
            trace.unlink()
    # Remove empty reservation directories, without touching other artifacts.
    try:
        artifact_directory.rmdir()
    except OSError:
        pass
