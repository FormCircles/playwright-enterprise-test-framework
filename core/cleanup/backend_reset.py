from __future__ import annotations


RESET_SUCCESS_STATUSES = {
    200,
    204,
}

RESET_UNAVAILABLE_STATUSES = {
    404,
    405,
}


def evaluate_reset_response(response) -> bool:
    """
    Evaluate a backend reset response.

    Returns:
        True when reset was completed.
        False when the endpoint is unavailable.

    Raises:
        AssertionError for unexpected failures.
    """

    if response.status in RESET_SUCCESS_STATUSES:
        return True

    if response.status in RESET_UNAVAILABLE_STATUSES:
        return False

    raise AssertionError(
        "Backend test-data reset failed. "
        f"Status: {response.status}. "
        f"Body: {response.text()}"
    )