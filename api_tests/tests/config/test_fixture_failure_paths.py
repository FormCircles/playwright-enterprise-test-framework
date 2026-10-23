"""Failure-path regression tests for PETF fixture lifecycles."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from playwright.sync_api import Page

from api_tests.fixtures.api_fixtures import (
    api_client as api_client_fixture,
)
from core.fixtures.api_fixtures import (
    api_request_context,
)
from ui_tests.fixtures.ui_fixtures import login_page


def make_api_fixture():
    """Create an isolated API fixture generator."""
    context = MagicMock()
    playwright = MagicMock()
    playwright.request.new_context.return_value = context

    settings = SimpleNamespace(request_timeout_ms=5000)

    generator = api_request_context.__wrapped__(
        playwright=playwright,
        base_url="http://127.0.0.1:8080",
        settings=settings,
    )

    return generator, context


def test_api_context_survives_dependent_setup() -> None:
    generator, context = make_api_fixture()

    assert next(generator) is context

    client = api_client_fixture.__wrapped__(
        api_request_context=context,
        auth_token="test-token",
    )

    assert client.request_context is context
    context.dispose.assert_not_called()

    generator.close()
    context.dispose.assert_called_once_with()


def test_api_context_cleanup_after_partial_setup_failure() -> None:
    generator, context = make_api_fixture()

    next(generator)

    try:
        raise RuntimeError("Dependent fixture setup failed")
    except RuntimeError:
        generator.close()

    context.dispose.assert_called_once_with()


def test_api_context_cleanup_failure_is_visible() -> None:
    generator, context = make_api_fixture()

    context.dispose.side_effect = RuntimeError("Context disposal failed")

    next(generator)

    with pytest.raises(RuntimeError, match="Context disposal failed"):
        generator.close()

    context.dispose.assert_called_once_with()


def test_api_context_repeated_execution() -> None:
    contexts = []

    for _ in range(3):
        generator, context = make_api_fixture()
        contexts.append(context)

        assert next(generator) is context
        generator.close()

        context.dispose.assert_called_once_with()

    assert len({id(context) for context in contexts}) == 3


def test_ui_fixture_does_not_close_page_on_success() -> None:
    page = MagicMock(spec=Page)

    result = login_page.__wrapped__(
        page=page,
        base_url="http://127.0.0.1:8080",
    )

    assert result.page is page
    page.close.assert_not_called()


def test_ui_fixture_does_not_close_page_on_setup_failure() -> None:
    page = MagicMock(spec=Page)

    page.set_default_timeout.side_effect = RuntimeError("UI setup failed")

    with pytest.raises(RuntimeError, match="UI setup failed"):
        login_page.__wrapped__(
            page=page,
            base_url="http://127.0.0.1:8080",
        )

    page.close.assert_not_called()
    page.context.close.assert_not_called()


def test_dependent_cleanup_precedes_context_disposal() -> None:
    """Verify simulated dependent cleanup precedes context disposal."""
    events = []

    @pytest.fixture
    def context_fixture():
        generator, context = make_api_fixture()
        next(generator)

        events.append("context_setup")
        yield context

        generator.close()
        events.append("context_disposed")

    @pytest.fixture
    def dependent_fixture(context_fixture):
        events.append("dependent_setup")
        yield context_fixture
        events.append("dependent_teardown")

    # Simulate fixture setup and cleanup in dependency order.
    context_generator = context_fixture.__wrapped__()
    context = next(context_generator)

    dependent_generator = dependent_fixture.__wrapped__(context)
    next(dependent_generator)

    with pytest.raises(StopIteration):
        next(dependent_generator)

    with pytest.raises(StopIteration):
        next(context_generator)

    assert events == [
        "context_setup",
        "dependent_setup",
        "dependent_teardown",
        "context_disposed",
    ]
