"""Regression tests for PETF artifact publication security."""

from __future__ import annotations

import zipfile
from pathlib import Path

import pytest

from core.diagnostics.artifact_security import (
    MAX_FILE_SIZE,
    ArtifactSecurityError,
    verify_artifact_security,
)


def write_file(root: Path, name: str, content: bytes) -> Path:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_clean_artifacts_are_accepted(tmp_path: Path) -> None:
    write_file(tmp_path, "reports/junit.xml", b"<testsuite tests='1'/>")
    write_file(tmp_path, "diagnostics/failure.log", b"AssertionError")
    write_file(tmp_path, "screenshots/failure.png", b"synthetic image")

    verify_artifact_security(tmp_path)


def test_bearer_token_is_rejected(tmp_path: Path) -> None:
    write_file(
        tmp_path,
        "diagnostics/failure.log",
        b"Authorization: Bearer PETF97_SYNTHETIC_TOKEN",
    )

    with pytest.raises(ArtifactSecurityError, match="PETF_SEC_BEARER"):
        verify_artifact_security(tmp_path)


def test_credential_assignment_is_rejected(tmp_path: Path) -> None:
    write_file(
        tmp_path,
        "reports/report.html",
        b"password=PETF97_SYNTHETIC_PASSWORD",
    )

    with pytest.raises(ArtifactSecurityError, match="PETF_SEC_CREDENTIAL"):
        verify_artifact_security(tmp_path)


def test_private_key_is_rejected(tmp_path: Path) -> None:
    write_file(
        tmp_path,
        "diagnostics/failure.txt",
        b"-----BEGIN PRIVATE KEY-----\nsynthetic\n",
    )

    with pytest.raises(ArtifactSecurityError, match="PETF_SEC_PRIVATE_KEY"):
        verify_artifact_security(tmp_path)


def test_clean_zip_is_accepted(tmp_path: Path) -> None:
    archive_path = tmp_path / "trace.zip"

    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("trace.json", '{"events": []}')

    verify_artifact_security(tmp_path)


def test_zip_with_secret_is_rejected(tmp_path: Path) -> None:
    archive_path = tmp_path / "trace.zip"

    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(
            "trace.network",
            "Authorization: Bearer PETF97_SYNTHETIC_TOKEN",
        )

    with pytest.raises(ArtifactSecurityError, match="PETF_SEC_BEARER"):
        verify_artifact_security(tmp_path)


def test_malformed_zip_is_rejected(tmp_path: Path) -> None:
    write_file(tmp_path, "trace.zip", b"not a valid ZIP")

    with pytest.raises(ArtifactSecurityError, match="Cannot safely inspect"):
        verify_artifact_security(tmp_path)


def test_oversized_file_is_rejected(tmp_path: Path) -> None:
    write_file(
        tmp_path,
        "diagnostics/large.log",
        b"x" * (MAX_FILE_SIZE + 1),
    )

    with pytest.raises(
        ArtifactSecurityError,
        match="inspection limit exceeded",
    ):
        verify_artifact_security(tmp_path)


def test_symlink_is_rejected(tmp_path: Path) -> None:
    target = write_file(tmp_path, "reports/junit.xml", b"<testsuite/>")
    (tmp_path / "linked.xml").symlink_to(target)

    with pytest.raises(ArtifactSecurityError, match="Symlink"):
        verify_artifact_security(tmp_path)


def test_nested_zip_with_secret_is_rejected(tmp_path: Path) -> None:
    from io import BytesIO

    inner = BytesIO()

    with zipfile.ZipFile(inner, "w") as archive:
        archive.writestr(
            "trace.network",
            "Authorization: Bearer PETF97_NESTED_SYNTHETIC_TOKEN",
        )

    with zipfile.ZipFile(tmp_path / "outer.zip", "w") as archive:
        archive.writestr("inner.zip", inner.getvalue())

    with pytest.raises(ArtifactSecurityError, match="PETF_SEC_BEARER"):
        verify_artifact_security(tmp_path)


def test_unsupported_format_is_rejected(tmp_path: Path) -> None:
    write_file(
        tmp_path,
        "diagnostics/unrecognized.bin",
        b"synthetic binary content",
    )

    with pytest.raises(
        ArtifactSecurityError,
        match="Unsupported artifact format",
    ):
        verify_artifact_security(tmp_path)


def test_broken_symlink_is_rejected(tmp_path: Path) -> None:
    (tmp_path / "broken.log").symlink_to(tmp_path / "does-not-exist.log")

    with pytest.raises(ArtifactSecurityError, match="Symlink"):
        verify_artifact_security(tmp_path)


def test_archive_nesting_limit_is_enforced(tmp_path: Path) -> None:
    from io import BytesIO

    content = b"safe synthetic content"

    for _ in range(4):
        buffer = BytesIO()

        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("nested.zip", content)

        content = buffer.getvalue()

    (tmp_path / "deep.zip").write_bytes(content)

    with pytest.raises(
        ArtifactSecurityError,
        match="nesting limit exceeded",
    ):
        verify_artifact_security(tmp_path)
