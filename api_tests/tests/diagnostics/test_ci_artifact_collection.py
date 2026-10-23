"""Regression tests for PETF CI artifact collection."""

from __future__ import annotations

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
        write_file(tmp_path, relative)

    result = collect_artifacts(run_id="ci-123-1", workspace=tmp_path)

    for relative in files:
        assert (result / "legacy" / relative).read_text() == "evidence"
        assert (tmp_path / relative).read_text() == "evidence"


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
