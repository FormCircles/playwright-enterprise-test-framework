from __future__ import annotations

from collections.abc import Iterator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from core.api.api_client import APIClient


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
    base_url: str,
    settings,
) -> Iterator[APIRequestContext]:
    """Own and dispose of the session's API request context.

    Dependent session fixtures finish before this fixture's teardown.
    """

    context = playwright.request.new_context(
        base_url=base_url,
        timeout=settings.request_timeout_ms,
    )

    try:
        yield context
    finally:
        context.dispose()


@pytest.fixture(scope="session")
def public_api_client(
    api_request_context: APIRequestContext,
) -> APIClient:
    """Return an unauthenticated API client."""

    return APIClient(
        request_context=api_request_context,
        auth_token=None,
    )
