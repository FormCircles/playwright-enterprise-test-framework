"""PETF-88 trace resource and cleanup failure regressions."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from core.diagnostics.trace_paths import (
    reserve_trace_directory,
    trace_artifact_directory,
)
from core.diagnostics.trace_retention import discard_successful_trace


def test_trace_resource_paths_isolate_workers_and_runs(tmp_path: Path):
    common = {"output_directory": tmp_path, "node_id": "ui::test_case[chromium]"}
    a = trace_artifact_directory(**common, run_id="run-a", worker_id="gw0")
    b = trace_artifact_directory(**common, run_id="run-a", worker_id="gw1")
    c = trace_artifact_directory(**common, run_id="run-b", worker_id="gw0")
    assert len({a, b, c}) == 3
    assert all(path.is_relative_to(tmp_path) for path in (a, b, c))


def test_repeated_resource_reservations_do_not_overwrite(tmp_path: Path):
    first = reserve_trace_directory(tmp_path / "run" / "gw0" / "hash")
    (first / "trace.zip").write_bytes(b"original")
    second = reserve_trace_directory(tmp_path / "run" / "gw0" / "hash")
    assert first != second
    assert (first / "trace.zip").read_bytes() == b"original"


def test_success_discards_only_traces(tmp_path: Path):
    folder = tmp_path / "artifact"
    folder.mkdir()
    (folder / "trace.zip").write_bytes(b"trace")
    (folder / "video.webm").write_bytes(b"video")
    discard_successful_trace(artifact_directory=folder, failed=False)
    assert not (folder / "trace.zip").exists()
    assert (folder / "video.webm").read_bytes() == b"video"


def test_failed_test_retains_trace(tmp_path: Path):
    folder = tmp_path / "artifact"
    folder.mkdir()
    (folder / "trace.zip").write_bytes(b"trace")
    discard_successful_trace(artifact_directory=folder, failed=True)
    assert (folder / "trace.zip").exists()


def test_trace_cleanup_io_error_does_not_mask_result(tmp_path: Path):
    folder = tmp_path / "artifact"
    folder.mkdir()
    (folder / "trace.zip").write_bytes(b"trace")
    with patch.object(
        Path, "unlink", side_effect=OSError("simulated artifact IO error")
    ):
        discard_successful_trace(artifact_directory=folder, failed=False)
    assert (folder / "trace.zip").exists()
