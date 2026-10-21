"""PETF-87 trace directory collision and retention regression tests."""

from pathlib import Path

from core.diagnostics.trace_paths import (
    reserve_trace_directory,
    trace_artifact_directory,
)
from core.diagnostics.trace_retention import discard_successful_trace


def test_trace_paths_are_stable_and_worker_isolated(tmp_path: Path):
    args = {
        "output_directory": tmp_path,
        "run_id": "run/1",
        "node_id": "suite::test[chromium]",
    }
    first = trace_artifact_directory(**args, worker_id="gw0")
    assert first == trace_artifact_directory(**args, worker_id="gw0")
    assert first != trace_artifact_directory(**args, worker_id="gw1")
    assert len(first.name) == 16
    assert first.is_relative_to(tmp_path)


def test_repeated_executions_never_overwrite(tmp_path: Path):
    base = tmp_path / "test-hash"
    first = reserve_trace_directory(base)
    (first / "trace.zip").write_bytes(b"old")
    second = reserve_trace_directory(base)
    assert first != second
    assert (first / "trace.zip").read_bytes() == b"old"
    assert second.is_dir()


def test_success_removes_only_trace_zips(tmp_path: Path):
    path = reserve_trace_directory(tmp_path / "test")
    (path / "trace.zip").write_bytes(b"trace")
    (path / "trace-2.zip").write_bytes(b"trace")
    (path / "video.webm").write_bytes(b"video")
    discard_successful_trace(artifact_directory=path, failed=False)
    assert not list(path.glob("trace*.zip"))
    assert (path / "video.webm").exists()


def test_failure_keeps_trace(tmp_path: Path):
    path = reserve_trace_directory(tmp_path / "test")
    (path / "trace.zip").write_bytes(b"trace")
    discard_successful_trace(artifact_directory=path, failed=True)
    assert (path / "trace.zip").exists()


def test_success_removes_empty_reserved_directory(tmp_path: Path):
    path = reserve_trace_directory(tmp_path / "test")
    discard_successful_trace(artifact_directory=path, failed=False)
    assert not path.exists()
