"""Regression tests for PETF CI artifact collection."""

from __future__ import annotations

import zipfile
from pathlib import Path

from scripts.collect_ci_artifacts import collect_artifacts


def write_file(root: Path, relative: str, content: str = "evidence") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_collects_reports_and_server_log(tmp_path):
    junit = write_file(tmp_path, "test-results/junit-results.xml", "junit")
    html = write_file(tmp_path, "test-results/report.html", "html")
    server = write_file(tmp_path, "sut/FastAPIMockApp/server.log", "server")

    result = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)

    assert (result / "reports/junit-results.xml").read_text() == "junit"
    assert (result / "reports/report.html").read_text() == "html"
    assert (result / "legacy/server-logs/server.log").read_text() == "server"
    assert junit.read_text() == "junit"
    assert html.read_text() == "html"
    assert server.read_text() == "server"


def test_preserves_screenshots_traces_and_diagnostics(tmp_path):
    files = [
        "test-results/screenshots/run/main/example.png",
        "test-results/playwright/run/main/test/trace.zip",
        "test-results/diagnostics/failure.txt",
    ]

    for relative in files:
        if relative.endswith(".zip"):
            trace_path = tmp_path / relative
            trace_path.parent.mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(trace_path, "w") as archive:
                archive.writestr(
                    "trace.json",
                    '{"events": [], "status": "synthetic"}',
                )
        else:
            write_file(tmp_path, relative)

    original_contents = {
        relative: (tmp_path / relative).read_bytes() for relative in files
    }

    result = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)

    for relative in files:
        assert (result / "legacy" / relative).read_bytes() == original_contents[
            relative
        ]

        assert (tmp_path / relative).read_bytes() == original_contents[relative]


def test_missing_artifacts_do_not_fail_collection(tmp_path):
    result = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)

    assert (result / "reports").is_dir()
    assert (result / "metadata").is_dir()


def test_independent_runs_are_isolated(tmp_path):
    write_file(tmp_path, "test-results/junit-results.xml")

    first = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)
    second = collect_artifacts(run_id="ci-124-1", workspace=tmp_path)

    assert first != second
    assert first.exists()
    assert second.exists()


def test_repeated_collection_preserves_existing_evidence(tmp_path):
    source = write_file(
        tmp_path,
        "test-results/junit-results.xml",
        "first",
    )

    first = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)

    source.write_text("second", encoding="utf-8")

    second = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)

    assert first != second
    assert (first / "reports/junit-results.xml").read_text() == "first"
    assert (second / "reports/junit-results.xml").read_text() == "second"


def test_rejects_sensitive_artifacts_and_preserves_sources(tmp_path):
    import pytest

    from core.diagnostics.artifact_security import ArtifactSecurityError

    original = write_file(
        tmp_path,
        "test-results/diagnostics/sensitive.log",
        "Authorization: Bearer PETF97_SYNTHETIC_SECRET",
    )

    with pytest.raises(ArtifactSecurityError, match="Bearer token"):
        collect_artifacts(run_id="ci-sensitive", workspace=tmp_path)

    assert original.read_text() == ("Authorization: Bearer PETF97_SYNTHETIC_SECRET")

    artifact_root = tmp_path / "artifacts"
    assert not list(artifact_root.iterdir())


def test_rejects_nested_zip_secret_and_cleans_staging(tmp_path):
    from io import BytesIO

    import pytest

    from core.diagnostics.artifact_security import ArtifactSecurityError

    inner = BytesIO()

    with zipfile.ZipFile(inner, "w") as archive:
        archive.writestr(
            "trace.network",
            "Authorization: Bearer PETF97_NESTED_SECRET",
        )

    trace = tmp_path / "test-results/playwright/run/gw0/trace.zip"
    trace.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(trace, "w") as archive:
        archive.writestr("nested.zip", inner.getvalue())

    original = trace.read_bytes()

    with pytest.raises(ArtifactSecurityError, match="Bearer token"):
        collect_artifacts(run_id="ci-nested", workspace=tmp_path)

    assert trace.read_bytes() == original
    assert not list((tmp_path / "artifacts").iterdir())
