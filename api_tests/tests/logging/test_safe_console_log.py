"""PETF-102 regression tests for safe CI console logging."""


import pytest

from scripts.safe_console_log import display_safe_log


def test_displays_safe_log(tmp_path, capsys):
    log = tmp_path / "safe.log"
    log.write_text("Application started successfully", encoding="utf-8")

    assert display_safe_log(log) is True
    assert "Application started successfully" in capsys.readouterr().out


@pytest.mark.parametrize(
    "sensitive_content",
    [
        "Authorization: Bearer synthetic-test-token-123456",
        "password=synthetic-password-123456",
        "-----BEGIN PRIVATE KEY-----",
    ],
    ids=[
        "bearer-token",
        "password-assignment",
        "private-key-header",
    ],
)
def test_rejects_sensitive_logs(tmp_path, capsys, sensitive_content):
    log = tmp_path / "sensitive.log"
    log.write_text(sensitive_content, encoding="utf-8")

    assert display_safe_log(log) is False

    output = capsys.readouterr().out
    assert sensitive_content not in output
    assert "withheld" in output.lower()


def test_rejects_missing_log(tmp_path, capsys):
    log = tmp_path / "missing.log"

    assert display_safe_log(log) is False
    assert "unavailable" in capsys.readouterr().out.lower()


def test_rejects_symlink(tmp_path, capsys):
    original = tmp_path / "original.log"
    original.write_text("Safe content", encoding="utf-8")

    link = tmp_path / "linked.log"
    link.symlink_to(original)

    assert display_safe_log(link) is False
    assert "unsafe" in capsys.readouterr().out.lower()


def test_rejects_oversized_log(tmp_path, capsys, monkeypatch):
    import scripts.safe_console_log as module

    log = tmp_path / "large.log"
    log.write_text("A" * 100, encoding="utf-8")

    monkeypatch.setattr(module, "MAX_FILE_SIZE", 50)

    assert display_safe_log(log) is False
    assert "withheld" in capsys.readouterr().out.lower()
