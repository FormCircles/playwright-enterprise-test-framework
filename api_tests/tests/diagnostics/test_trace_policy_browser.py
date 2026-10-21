"""PETF-88 real Chromium trace lifecycle regression tests.

Requires installed Chromium. Nested pytest runs isolate each scenario.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import uuid
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def run_probe(tmp_path: Path, code: str, *, policy: str, parallel: bool = False):
    name = "test_petf88_" + uuid.uuid4().hex[:12] + ".py"
    probe = ROOT / "ui_tests" / name
    output = tmp_path / "native-artifacts"
    probe.write_text(code)
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        str(probe),
        "-q",
        "--tb=short",
        "--browser",
        "chromium",
        "--petf-trace=" + policy,
    ]
    if parallel:
        cmd.extend(["-n", "2"])
    try:
        result = subprocess.run(
            cmd, check=False, cwd=ROOT, capture_output=True, text=True, timeout=60
        )
        return result, output, probe
    finally:
        probe.unlink(missing_ok=True)


def traces_for_run(before: set[Path]):
    return set((ROOT / "test-results" / "playwright").rglob("trace*.zip")) - before


def test_disabled_does_not_create_traces(tmp_path: Path):
    before = set((ROOT / "test-results" / "playwright").rglob("trace*.zip"))
    result, _, _ = run_probe(
        tmp_path,
        'def test_ok(page):\n    page.set_content("<p>ok</p>")\n',
        policy="off",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert not traces_for_run(before)


def test_success_discards_trace(tmp_path: Path):
    before = set((ROOT / "test-results" / "playwright").rglob("trace*.zip"))
    result, _, _ = run_probe(
        tmp_path,
        'def test_ok(page):\n    page.set_content("<p>ok</p>")\n',
        policy="on-failure",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert not traces_for_run(before)


def test_failure_retains_readable_trace_and_original_assertion(tmp_path: Path):
    before = set((ROOT / "test-results" / "playwright").rglob("trace*.zip"))
    result, _, _ = run_probe(
        tmp_path,
        'def test_fail(page):\n    page.set_content("<p>ok</p>")\n    assert False, "PETF88_ORIGINAL_FAILURE"\n',
        policy="on-failure",
    )
    assert result.returncode != 0
    assert "PETF88_ORIGINAL_FAILURE" in result.stdout
    traces = traces_for_run(before)
    assert len(traces) == 1, traces
    with zipfile.ZipFile(next(iter(traces))) as archive:
        assert archive.testzip() is None


def test_teardown_failure_retains_trace(tmp_path: Path):
    before = set((ROOT / "test-results" / "playwright").rglob("trace*.zip"))
    code = 'import pytest\n@pytest.fixture\ndef broken():\n    yield\n    raise RuntimeError("PETF88_TEARDOWN_FAILURE")\ndef test_ok(page, broken):\n    page.set_content("<p>ok</p>")\n'
    result, _, _ = run_probe(tmp_path, code, policy="on-failure")
    assert result.returncode != 0
    assert "PETF88_TEARDOWN_FAILURE" in result.stdout
    assert len(traces_for_run(before)) == 1


def test_parallel_failures_have_distinct_worker_artifacts(tmp_path: Path):
    before = set((ROOT / "test-results" / "playwright").rglob("trace*.zip"))
    code = 'import pytest\n@pytest.mark.parametrize("n", range(4))\ndef test_fail(page, n):\n    page.set_content("<p>ok</p>")\n    assert False, "PETF88_PARALLEL_FAILURE"\n'
    result, _, _ = run_probe(tmp_path, code, policy="on-failure", parallel=True)
    assert result.returncode != 0
    assert "PETF88_PARALLEL_FAILURE" in result.stdout
    traces = traces_for_run(before)
    assert len(traces) == 4, (len(traces), result.stdout)
    assert len({p.parent for p in traces}) == 4
    assert len({p.parent.parent.name for p in traces}) >= 2


@pytest.mark.skipif(
    os.environ.get("PETF88_INTERRUPT") != "1",
    reason="opt-in interrupt probe; set PETF88_INTERRUPT=1",
)
def test_interrupt_preserves_original_interrupt_and_no_corrupt_archives(tmp_path: Path):
    name = "test_petf88_interrupt_" + uuid.uuid4().hex[:12] + ".py"
    probe = ROOT / "ui_tests" / name
    probe.write_text(
        'import time\ndef test_interrupt(page):\n    page.set_content("<p>ready</p>")\n    print("PETF88_READY", flush=True)\n    time.sleep(30)\n'
    )
    before = set((ROOT / "test-results" / "playwright").rglob("trace*.zip"))
    cmd = [
        sys.executable,
        "-u",
        "-m",
        "pytest",
        str(probe),
        "-s",
        "-q",
        "--browser",
        "chromium",
        "--petf-trace=on-failure",
    ]
    process = subprocess.Popen(
        cmd,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    try:
        deadline = time.monotonic() + 20
        ready = False
        # Wait for browser initialization before sending SIGINT.
        import select

        while time.monotonic() < deadline:
            readable, _, _ = select.select([process.stdout], [], [], 0.5)
            if readable:
                line = process.stdout.readline()
                if "PETF88_READY" in line:
                    ready = True
                    break
            if process.poll() is not None:
                break
        assert ready, "Browser did not reach interrupt checkpoint"
        process.send_signal(signal.SIGINT)
        stdout, _ = process.communicate(timeout=20)
        assert process.returncode != 0
        assert "KeyboardInterrupt" in stdout or "Interrupted" in stdout, stdout[-2000:]
        for trace in (
            set((ROOT / "test-results" / "playwright").rglob("trace*.zip")) - before
        ):
            with zipfile.ZipFile(trace) as archive:
                assert archive.testzip() is None
    finally:
        if process.poll() is None:
            process.kill()
            process.communicate()
        probe.unlink(missing_ok=True)
