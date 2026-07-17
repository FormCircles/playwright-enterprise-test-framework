from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.logging.sanitization import sanitize_text


MAX_DIAGNOSTIC_LENGTH = 20_000


@dataclass(frozen=True)
class FailureDiagnostics:
    """Sanitized diagnostic information for a failed test."""

    node_id: str
    phase: str
    environment: str
    base_url: str
    error: str
    captured_logs: str

    def render(self) -> str:
        """Render diagnostics as plain text."""

        sections = [
            f"Test: {self.node_id}",
            f"Phase: {self.phase}",
            f"Environment: {self.environment}",
            f"Base URL: {self.base_url}",
            "",
            "Failure:",
            self.error or "No failure details were available.",
            "",
            "Captured logs:",
            self.captured_logs or "No log output was captured.",
        ]

        rendered = "\n".join(sections)

        if len(rendered) > MAX_DIAGNOSTIC_LENGTH:
            rendered = (
                rendered[:MAX_DIAGNOSTIC_LENGTH]
                + "\n\n[Diagnostics truncated]"
            )

        return sanitize_text(rendered)


def extract_captured_logs(report: Any) -> str:
    """Extract captured logging sections from a pytest report."""

    log_sections: list[str] = []

    for section_name, section_content in report.sections:
        if "log" not in section_name.lower():
            continue

        log_sections.append(
            f"[{section_name}]\n{section_content}"
        )

    return sanitize_text("\n\n".join(log_sections))


def build_failure_diagnostics(
    *,
    item: Any,
    report: Any,
) -> FailureDiagnostics:
    """Build sanitized diagnostics for one failed pytest phase."""

    settings = item.funcargs.get("settings")

    environment = getattr(settings, "env", "unknown")
    base_url = getattr(settings, "base_url", "unknown")

    error = sanitize_text(str(report.longrepr))
    captured_logs = extract_captured_logs(report)

    return FailureDiagnostics(
        node_id=report.nodeid,
        phase=report.when,
        environment=environment,
        base_url=base_url,
        error=error,
        captured_logs=captured_logs,
    )


def write_failure_diagnostics(
    *,
    diagnostics: FailureDiagnostics,
    output_directory: Path,
) -> Path:
    """Write diagnostics to a uniquely named text file."""

    output_directory.mkdir(parents=True, exist_ok=True)

    safe_test_name = (
        diagnostics.node_id
        .replace("/", "_")
        .replace("\\", "_")
        .replace("::", "__")
        .replace("[", "_")
        .replace("]", "_")
    )

    output_path = output_directory / (
        f"{safe_test_name}_{diagnostics.phase}.txt"
    )

    output_path.write_text(
        diagnostics.render(),
        encoding="utf-8",
    )

    return output_path
