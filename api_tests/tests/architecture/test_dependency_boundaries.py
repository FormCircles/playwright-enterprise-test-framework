"""Regression checks for PETF core dependency boundaries."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CORE_DIRECTORY = REPOSITORY_ROOT / "core"

PROHIBITED_ROOTS = frozenset(
    {
        "api_tests",
        "ui_tests",
        "sut",
    }
)


def prohibited_imports(source: str) -> list[tuple[int, str]]:
    """Return prohibited imports as (line number, module name) pairs."""
    tree = ast.parse(source)
    violations: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                continue
            modules = [node.module] if node.module else []
        else:
            continue

        for module in modules:
            if module.split(".", maxsplit=1)[0] in PROHIBITED_ROOTS:
                violations.append((node.lineno, module))

    return violations


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("import api_tests.services.devices_service", True),
        ("from api_tests.services import DevicesService", True),
        ("import ui_tests.pages.login_page", True),
        ("from ui_tests.pages.login_page import LoginPage", True),
        ("import sut.FastAPIMockApp", True),
        ("import core.api.api_client", False),
        ("from core.config.settings import Settings", False),
        ("import pytest", False),
        ("import api_tests_helper", False),
    ],
)
def test_dependency_scanner_classifies_imports(
    source: str,
    expected: bool,
) -> None:
    """Recognize prohibited imports without rejecting unrelated modules."""
    assert bool(prohibited_imports(source)) is expected


def test_core_has_no_reference_sut_dependencies() -> None:
    """PETF core must not import reference application implementations."""
    violations: list[str] = []

    for path in sorted(CORE_DIRECTORY.rglob("*.py")):
        relative_path = path.relative_to(REPOSITORY_ROOT)
        source = path.read_text(encoding="utf-8")

        for line_number, module in prohibited_imports(source):
            violations.append(f"{relative_path}:{line_number}: {module}")

    assert not violations, (
        "PETF core contains prohibited reference-SUT dependencies:\n"
        + "\n".join(violations)
    )
