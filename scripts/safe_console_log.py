"""Safely display diagnostic logs in CI consoles."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from core.diagnostics.artifact_security import (
    MAX_FILE_SIZE,
    ArtifactSecurityError,
    verify_text_content,
)


def display_safe_log(path: Path) -> bool:
    """Display a log only when its contents pass security checks."""

    if not path.is_file() or path.is_symlink():
        print("Diagnostic log unavailable or unsafe.")
        return False

    if path.stat().st_size > MAX_FILE_SIZE:
        print("Diagnostic log withheld: security verification failed.")
        return False

    try:
        content = path.read_bytes()
        verify_text_content(content, path.name)
    except (ArtifactSecurityError, OSError):
        print("Diagnostic log withheld: security verification failed.")
        return False

    sys.stdout.write(content.decode("utf-8", errors="replace"))
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    raise SystemExit(0 if display_safe_log(args.path) else 1)


if __name__ == "__main__":
    main()
