from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from core.diagnostics.failure_diagnostics import (
    FailureDiagnostics,
    build_failure_diagnostics,
    extract_captured_logs,
    write_failure_diagnostics,
)


def test_extracts_captured_log_sections() -> None:
    report = SimpleNamespace(
        sections=[
            (
                "Captured stdout call",
                "normal output",
            ),
            (
                "Captured log call",
                "API request completed status=500",
            ),
        ]
    )

    result = extract_captured_logs(report)

    assert "Captured log call" in result
    assert "status=500" in result
    assert "normal output" not in result


def test_builds_failure_diagnostics() -> None:
    settings = SimpleNamespace(
        env="ci",
        base_url="http://127.0.0.1:8080",
    )

    item = SimpleNamespace(
        funcargs={
            "settings": settings,
        }
    )

    report = SimpleNamespace(
        nodeid="api_tests/tests/test_example.py::test_failure",
        when="call",
        longrepr="AssertionError: expected 200",
        sections=[
            (
                "Captured log call",
                "API request completed status=500",
            ),
        ],
    )

    diagnostics = build_failure_diagnostics(
        item=item,
        report=report,
    )

    assert diagnostics.environment == "ci"
    assert diagnostics.base_url == "http://127.0.0.1:8080"
    assert diagnostics.phase == "call"
    assert "expected 200" in diagnostics.error
    assert "status=500" in diagnostics.captured_logs


def test_masks_secrets_in_failure_diagnostics() -> None:
    item = SimpleNamespace(
        funcargs={
            "settings": SimpleNamespace(
                env="ci",
                base_url="http://127.0.0.1:8080",
            ),
        }
    )

    report = SimpleNamespace(
        nodeid="test_secret.py::test_failure",
        when="call",
        longrepr=(
            "Request failed using "
            "Bearer secret-token-value"
        ),
        sections=[
            (
                "Captured log call",
                "Authorization: Bearer another-secret-token",
            ),
        ],
    )

    diagnostics = build_failure_diagnostics(
        item=item,
        report=report,
    ).render()

    assert "secret-token-value" not in diagnostics
    assert "another-secret-token" not in diagnostics
    assert "***REDACTED***" in diagnostics


def test_writes_diagnostic_file(
    tmp_path: Path,
) -> None:
    diagnostics = FailureDiagnostics(
        node_id="tests/test_example.py::test_failure",
        phase="call",
        environment="local",
        base_url="http://127.0.0.1:8080",
        error="AssertionError",
        captured_logs="status=500",
    )

    output_path = write_failure_diagnostics(
        diagnostics=diagnostics,
        output_directory=tmp_path,
    )

    assert output_path.exists()

    contents = output_path.read_text(
        encoding="utf-8",
    )

    assert "test_failure" in contents
    assert "AssertionError" in contents
    assert "status=500" in contents
