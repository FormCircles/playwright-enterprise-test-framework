from __future__ import annotations
from jsonschema import ValidationError, validate

from collections.abc import Iterable
from typing import Any


def assert_status_code(response, expected_status: int) -> None:
    """Assert an API response has the expected HTTP status code."""

    assert response.status == expected_status, (
        f"Expected status {expected_status}, got {response.status}. "
        f"Body: {response.text()}"
    )


def assert_required_fields(
    payload: dict[str, Any],
    required_fields: Iterable[str],
) -> None:
    """Assert a response payload contains all required fields."""

    missing_fields = [
        field
        for field in required_fields
        if field not in payload
    ]

    assert not missing_fields, (
        f"Response is missing required fields: {missing_fields}. "
        f"Payload: {payload}"
    )


def assert_error_response(
    response,
    expected_status: int,
    required_fields: Iterable[str] = ("detail",),
) -> dict[str, Any]:
    """Assert a standard error response and return the parsed body."""

    assert_status_code(response, expected_status)

    body = response.json()

    assert isinstance(body, dict), (
        f"Expected error response body to be an object, got: {body}"
    )

    assert_required_fields(body, required_fields)

    return body


def assert_success_response(
    response,
    expected_status: int,
    required_fields: Iterable[str] = (),
) -> dict[str, Any]:
    """Assert a successful JSON response and return the parsed body."""

    assert_status_code(response, expected_status)

    body = response.json()

    assert isinstance(body, dict), (
        f"Expected success response body to be an object, got: {body}"
    )

    if required_fields:
        assert_required_fields(body, required_fields)

    return body

def assert_matches_schema(
    payload: Any,
    schema: dict[str, Any],
) -> None:
    """Assert that a JSON payload matches the expected JSON Schema."""

    try:
        validate(instance=payload, schema=schema)
    except ValidationError as error:
        location = (
            " -> ".join(str(part) for part in error.absolute_path)
            or "<root>"
        )

        raise AssertionError(
            "Response payload does not match the expected schema. "
            f"Location: {location}. "
            f"Reason: {error.message}. "
            f"Payload: {payload}"
        ) from error