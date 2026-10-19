"""Regression tests for PETF API request-context ownership."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from core.fixtures.api_fixtures import api_request_context


def create_fixture():
    """Construct the fixture generator with mocked dependencies."""
    context = MagicMock()
    playwright = MagicMock()
    playwright.request.new_context.return_value = context

    settings = SimpleNamespace(request_timeout_ms=5000)

    generator = api_request_context.__wrapped__(
        playwright=playwright,
        base_url="http://127.0.0.1:8080",
        settings=settings,
    )

    return generator, playwright, context


def test_context_is_created_with_configured_settings() -> None:
    """The context uses PETF's configured URL and timeout."""
    generator, playwright, context = create_fixture()

    assert next(generator) is context

    playwright.request.new_context.assert_called_once_with(
        base_url="http://127.0.0.1:8080",
        timeout=5000,
    )

    generator.close()


def test_context_remains_open_until_teardown() -> None:
    """The owning fixture must not dispose of an active context."""
    generator, _, context = create_fixture()

    next(generator)

    context.dispose.assert_not_called()

    generator.close()

    context.dispose.assert_called_once_with()


def test_context_is_disposed_on_normal_completion() -> None:
    """Normal fixture teardown disposes of the context exactly once."""
    generator, _, context = create_fixture()

    next(generator)

    with pytest.raises(StopIteration):
        next(generator)

    context.dispose.assert_called_once_with()


def test_context_is_disposed_when_fixture_is_closed() -> None:
    """Generator close triggers the fixture's finally block."""
    generator, _, context = create_fixture()

    next(generator)
    generator.close()

    context.dispose.assert_called_once_with()


def test_context_is_disposed_after_test_failure() -> None:
    """A failure while the fixture is active must not leak resources."""
    generator, _, context = create_fixture()

    next(generator)

    try:
        raise RuntimeError("Simulated test failure")
    except RuntimeError:
        generator.close()

    context.dispose.assert_called_once_with()


def test_context_disposal_failure_is_not_silenced() -> None:
    """Cleanup errors remain visible instead of being swallowed."""
    generator, _, context = create_fixture()

    context.dispose.side_effect = RuntimeError("Simulated disposal failure")

    next(generator)

    with pytest.raises(
        RuntimeError,
        match="Simulated disposal failure",
    ):
        generator.close()

    context.dispose.assert_called_once_with()
