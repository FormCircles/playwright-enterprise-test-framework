"""Regression tests for the canonical PETF artifact directory contract."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.diagnostics.artifact_paths import (
    artifact_kind_directory,
    case_artifact_directory,
    ensure_artifact_directory,
    metadata_artifact_directory,
    report_artifact_directory,
    reserve_artifact_directory,
    run_artifact_directory,
    worker_artifact_directory,
)

IDENTITY = {
    "run_id": "run-123",
    "worker_id": "gw0",
    "suite_id": "ui",
    "node_id": "ui_tests/test_login.py::test_login[chromium]",
}


def test_run_directory_is_deterministic(tmp_path: Path) -> None:
    first = run_artifact_directory(run_id="run-123", root=tmp_path)
    second = run_artifact_directory(run_id="run-123", root=tmp_path)

    assert first == second
    assert first == tmp_path / "run-123"


def test_run_directories_are_isolated(tmp_path: Path) -> None:
    first = run_artifact_directory(run_id="run-1", root=tmp_path)
    second = run_artifact_directory(run_id="run-2", root=tmp_path)

    assert first != second


def test_worker_directories_are_isolated(tmp_path: Path) -> None:
    first = worker_artifact_directory(run_id="run-1", worker_id="gw0", root=tmp_path)
    second = worker_artifact_directory(run_id="run-1", worker_id="gw1", root=tmp_path)

    assert first != second


def test_suite_directories_are_isolated(tmp_path: Path) -> None:
    first = case_artifact_directory(**IDENTITY, root=tmp_path)
    second = case_artifact_directory(
        **{**IDENTITY, "suite_id": "api"},
        root=tmp_path,
    )

    assert first != second


def test_parameterized_tests_are_isolated(tmp_path: Path) -> None:
    first = case_artifact_directory(**IDENTITY, root=tmp_path)
    second = case_artifact_directory(
        **{
            **IDENTITY,
            "node_id": "ui_tests/test_login.py::test_login[firefox]",
        },
        root=tmp_path,
    )

    assert first != second


def test_test_paths_are_stable(tmp_path: Path) -> None:
    first = case_artifact_directory(**IDENTITY, root=tmp_path)
    second = case_artifact_directory(**IDENTITY, root=tmp_path)

    assert first == second


@pytest.mark.parametrize(
    "kind",
    ["logs", "screenshots", "traces", "attachments"],
)
def test_supported_artifact_kinds(kind: str, tmp_path: Path) -> None:
    path = artifact_kind_directory(
        **IDENTITY,
        kind=kind,
        root=tmp_path,
    )

    assert path.name == kind
    assert path.parent == case_artifact_directory(
        **IDENTITY,
        root=tmp_path,
    )


def test_unknown_artifact_kind_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Unsupported artifact kind"):
        artifact_kind_directory(
            **IDENTITY,
            kind="../../outside",
            root=tmp_path,
        )


def test_directory_creation_is_repeatable(tmp_path: Path) -> None:
    path = case_artifact_directory(**IDENTITY, root=tmp_path)

    assert ensure_artifact_directory(path) == path
    assert ensure_artifact_directory(path) == path
    assert path.is_dir()


def test_reservation_preserves_existing_evidence(tmp_path: Path) -> None:
    base = artifact_kind_directory(
        **IDENTITY,
        kind="traces",
        root=tmp_path,
    )

    first = reserve_artifact_directory(base)
    (first / "trace.zip").write_bytes(b"original")

    second = reserve_artifact_directory(base)

    assert first != second
    assert (first / "trace.zip").read_bytes() == b"original"
    assert second.is_dir()


def test_untrusted_identifiers_cannot_escape_root(tmp_path: Path) -> None:
    path = case_artifact_directory(
        run_id="../../outside",
        worker_id="../worker",
        suite_id="../../suite",
        node_id="../../secrets",
        root=tmp_path,
    )

    assert path.is_relative_to(tmp_path)
    assert ".." not in path.relative_to(tmp_path).parts


def test_report_and_metadata_directories(tmp_path: Path) -> None:
    reports = report_artifact_directory(run_id="run-1", root=tmp_path)
    metadata = metadata_artifact_directory(run_id="run-1", root=tmp_path)

    assert reports == tmp_path / "run-1" / "reports"
    assert metadata == tmp_path / "run-1" / "metadata"
