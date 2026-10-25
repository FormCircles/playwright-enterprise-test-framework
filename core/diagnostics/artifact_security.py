"""Pre-publication security checks for PETF artifacts."""

from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

from core.logging.sanitization import BEARER_TOKEN_PATTERN

MAX_FILE_SIZE = 25 * 1024 * 1024
MAX_ARCHIVE_SIZE = 100 * 1024 * 1024
MAX_ARCHIVE_DEPTH = 3

TEXT_SUFFIXES = frozenset(
    {
        ".txt",
        ".log",
        ".xml",
        ".html",
        ".json",
        ".jsonl",
        ".yaml",
        ".yml",
        ".csv",
        ".md",
        ".network",
        ".trace",
        ".stacks",
        ".css",
        ".js",
        ".map",
        ".svg",
    }
)

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg"})

CREDENTIAL_PATTERN = re.compile(
    rb"(?i)\b(?:password|passwd|secret|api[_-]?key|"
    rb"access[_-]?token|refresh[_-]?token|"
    rb"authorization|cookie)\s*[:=]\s*"
    rb"""["']?[^\s"'<>]{6,}"""
)

PRIVATE_KEY_PATTERN = re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")


class ArtifactSecurityError(RuntimeError):
    """Raised when artifact publication is unsafe."""


def _check_content(content: bytes, label: str) -> None:
    """Reject recognizable credentials without exposing values."""
    if BEARER_TOKEN_PATTERN.search(content.decode("utf-8", errors="replace")):
        raise ArtifactSecurityError(f"Bearer token detected: {label}")

    if CREDENTIAL_PATTERN.search(content):
        raise ArtifactSecurityError(f"Credential detected: {label}")

    if PRIVATE_KEY_PATTERN.search(content):
        raise ArtifactSecurityError(f"Private key detected: {label}")



def verify_text_content(content: bytes, label: str) -> None:
    """Verify text content without exposing sensitive values."""
    _check_content(content, label)


def _check_zip(
    content: bytes,
    label: str,
    *,
    depth: int,
    budget: list[int],
) -> None:
    """Inspect nested ZIP contents with cumulative limits."""
    if depth > MAX_ARCHIVE_DEPTH:
        raise ArtifactSecurityError(f"Archive nesting limit exceeded: {label}")

    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue

                if member.file_size > MAX_FILE_SIZE:
                    raise ArtifactSecurityError(f"Archive member too large: {label}")

                budget[0] += member.file_size

                if budget[0] > MAX_ARCHIVE_SIZE:
                    raise ArtifactSecurityError(
                        f"Archive inspection limit exceeded: {label}"
                    )

                with archive.open(member) as stream:
                    data = stream.read(MAX_FILE_SIZE + 1)

                if len(data) > MAX_FILE_SIZE:
                    raise ArtifactSecurityError(f"Archive member too large: {label}")

                member_label = f"{label}!{member.filename}"

                if member.filename.lower().endswith(".zip"):
                    _check_zip(
                        data,
                        member_label,
                        depth=depth + 1,
                        budget=budget,
                    )
                else:
                    _check_content(data, member_label)

    except ArtifactSecurityError:
        raise
    except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
        raise ArtifactSecurityError(f"Cannot safely inspect archive: {label}") from exc


def verify_artifact_security(root: Path) -> None:
    """Reject unsafe artifacts before publication."""
    if not root.is_dir() or root.is_symlink():
        raise ArtifactSecurityError("Artifact root must be a real directory")

    budget = [0]

    for path in root.rglob("*"):
        label = str(path.relative_to(root))

        if path.is_symlink():
            raise ArtifactSecurityError(f"Symlink artifact not permitted: {label}")

        if not path.is_file():
            continue

        if path.stat().st_size > MAX_FILE_SIZE:
            raise ArtifactSecurityError(f"Artifact inspection limit exceeded: {label}")

        suffix = path.suffix.lower()

        if suffix == ".zip":
            _check_zip(
                path.read_bytes(),
                label,
                depth=1,
                budget=budget,
            )
        elif suffix in TEXT_SUFFIXES:
            _check_content(path.read_bytes(), label)
        elif suffix in IMAGE_SUFFIXES:
            # Image contents are not inspected for embedded secrets.
            # Producer-side controls are required.
            continue
        else:
            raise ArtifactSecurityError(f"Unsupported artifact format: {label}")
