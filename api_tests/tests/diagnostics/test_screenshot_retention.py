"""Cross-process screenshot artifact retention verification."""

import os
import subprocess
import sys
from pathlib import Path


def test_screenshots_survive_separate_pytest_processes(tmp_path):
    """A later pytest process must preserve an earlier run's evidence."""
    output_dir = tmp_path / "screenshots"
    probe = tmp_path / "probe.py"

    probe.write_text(
        """
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock
from playwright.sync_api import Page
from core.diagnostics.failure_screenshots import capture_failure_screenshot

page = MagicMock(spec=Page)
page.is_closed.return_value = False
page.screenshot.side_effect = lambda *, path, full_page: Path(path).write_bytes(b"evidence")

item = MagicMock()
item.path = Path("ui_tests/tests/test_probe.py")
item.get_closest_marker.return_value = None
item.funcargs = {"page": page}

report = SimpleNamespace(
    failed=True,
    when="call",
    nodeid="test_probe.py::test_failure",
)

import sys

result = capture_failure_screenshot(
    item=item,
    report=report,
    output_directory=Path(sys.argv[1]),
    run_id=sys.argv[2],
    worker_id="gw0",
)

assert result is not None
assert result.exists()
"""
    )

    for run_id in ("run-A", "run-B"):
        subprocess.run(
            [sys.executable, str(probe), str(output_dir), run_id],
            check=True,
            capture_output=True,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[3])},
            text=True,
        )

    screenshots = list(output_dir.rglob("*.png"))

    assert len(screenshots) == 2
    assert all(path.read_bytes() == b"evidence" for path in screenshots)
    assert {path.parent.parent.name for path in screenshots} == {
        "run-A",
        "run-B",
    }
