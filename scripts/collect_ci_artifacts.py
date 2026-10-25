"""Collect legacy PETF outputs into a run-scoped CI publication directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

from core.diagnostics.artifact_paths import (
    ensure_artifact_directory,
    reserve_artifact_directory,
    run_artifact_directory,
)
from core.diagnostics.artifact_security import verify_artifact_security

REPORT_FILES = (
    Path("test-results/junit-results.xml"),
    Path("test-results/report.html"),
    Path("test-results/smoke-junit-results.xml"),
    Path("test-results/smoke-report.html"),
)

LEGACY_DIRECTORIES = (
    Path("test-results/diagnostics"),
    Path("test-results/screenshots"),
    Path("test-results/playwright"),
    Path("test-results/logs"),
)

SERVER_LOG = Path("sut/FastAPIMockApp/server.log")


def collect_artifacts(*, run_id: str, workspace: Path) -> Path:
    """Stage available artifacts without modifying their source files."""
    root = workspace / "artifacts"
    run_dir = reserve_artifact_directory(
        run_artifact_directory(run_id=run_id, root=root)
    )

    reports_dir = ensure_artifact_directory(run_dir / "reports")
    ensure_artifact_directory(run_dir / "metadata")

    for relative_path in REPORT_FILES:
        source = workspace / relative_path
        if source.is_file():
            shutil.copy2(source, reports_dir / source.name)

    legacy_dir = run_dir / "legacy"

    for relative_path in LEGACY_DIRECTORIES:
        source = workspace / relative_path
        if source.is_dir():
            destination = legacy_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination)

    source_log = workspace / SERVER_LOG
    if source_log.is_file():
        destination = legacy_dir / "server-logs" / source_log.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_log, destination)

    try:
        verify_artifact_security(run_dir)
    except Exception:
        shutil.rmtree(run_dir)
        raise

    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    args = parser.parse_args()

    result = collect_artifacts(
        run_id=args.run_id,
        workspace=args.workspace.resolve(),
    )
    print(f"Collected CI artifacts: {result}")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with Path(github_output).open("a", encoding="utf-8") as output:
            output.write(f"artifact_path={result}\n")


if __name__ == "__main__":
    main()
