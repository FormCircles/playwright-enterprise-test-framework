"""Regression tests for deterministic screenshot paths."""

from pathlib import Path

from core.diagnostics.screenshot_paths import screenshot_artifact_path

BASE = Path("test-results/screenshots")


def build(run="run-1", worker="gw0", node="ui_tests/test_login.py::test_login"):
    return screenshot_artifact_path(
        output_directory=BASE,
        run_id=run,
        worker_id=worker,
        node_id=node,
    )


def test_same_identity_produces_same_path():
    assert build() == build()


def test_different_workers_produce_different_paths():
    assert build(worker="gw0") != build(worker="gw1")


def test_different_runs_produce_different_paths():
    assert build(run="run-1") != build(run="run-2")


def test_different_tests_produce_different_paths():
    assert build(node="test_a.py::test_login") != build(node="test_b.py::test_login")


def test_parameterized_tests_produce_different_paths():
    assert build(node="test_a.py::test_login[one]") != build(
        node="test_a.py::test_login[two]"
    )


def test_sanitized_name_collisions_are_distinguished():
    assert build(node="test_a.py::test_a/b") != build(node="test_a.py::test_a?b")


def test_untrusted_identifiers_cannot_escape_directory():
    path = build(
        run="../../outside",
        worker="../gw0",
        node="../../secrets::test/../../escape",
    )

    assert path.is_relative_to(BASE)
    assert ".." not in path.relative_to(BASE).parts
    assert path.suffix == ".png"


def test_long_run_identifiers_remain_distinct():
    prefix = "a" * 100

    assert build(run=prefix + "one") != build(run=prefix + "two")


def test_long_worker_identifiers_remain_distinct():
    prefix = "w" * 100

    assert build(worker=prefix + "one") != build(worker=prefix + "two")


def test_sanitized_run_identifiers_remain_distinct():
    assert build(run="run/a") != build(run="run?a")


def test_sanitized_worker_identifiers_remain_distinct():
    assert build(worker="worker/a") != build(worker="worker?a")


def test_empty_and_literal_unknown_identifiers_remain_distinct():
    assert build(run="") != build(run="unknown")
