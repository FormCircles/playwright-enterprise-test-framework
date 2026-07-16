from __future__ import annotations

from unittest.mock import Mock

import pytest

from core.cleanup.backend_reset import evaluate_reset_response


def make_response(
    status: int,
    body: str = "",
):
    response = Mock()
    response.status = status
    response.text.return_value = body
    return response


@pytest.mark.parametrize("status", [200, 204])
def test_reset_response_reports_success(status):
    response = make_response(status)

    assert evaluate_reset_response(response) is True


@pytest.mark.parametrize("status", [404, 405])
def test_reset_response_reports_unavailable(status):
    response = make_response(status)

    assert evaluate_reset_response(response) is False


def test_reset_response_rejects_unexpected_failure():
    response = make_response(
        500,
        "Internal server error",
    )

    with pytest.raises(AssertionError) as error:
        evaluate_reset_response(response)

    message = str(error.value)

    assert "Status: 500" in message
    assert "Internal server error" in message