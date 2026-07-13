from __future__ import annotations
from core.assertions.api_assertions import assert_matches_schema

from unittest.mock import Mock

import pytest

from core.assertions.api_assertions import (
    assert_error_response,
    assert_required_fields,
    assert_status_code,
    assert_success_response,
)


def make_response(
    status: int,
    body: object,
    text: str = "",
):
    response = Mock()
    response.status = status
    response.json.return_value = body
    response.text.return_value = text or str(body)
    return response


def test_assert_status_code_passes_for_expected_status():
    response = make_response(200, {})

    assert_status_code(response, 200)


def test_assert_status_code_reports_actual_status_and_body():
    response = make_response(
        500,
        {"detail": "Internal error"},
    )

    with pytest.raises(AssertionError) as error:
        assert_status_code(response, 200)

    message = str(error.value)

    assert "Expected status 200" in message
    assert "got 500" in message
    assert "Internal error" in message


def test_assert_required_fields_passes_when_fields_exist():
    payload = {
        "id": 1,
        "name": "Device",
        "status": "active",
    }

    assert_required_fields(
        payload,
        ("id", "name", "status"),
    )


def test_assert_required_fields_reports_missing_fields():
    payload = {
        "id": 1,
    }

    with pytest.raises(AssertionError) as error:
        assert_required_fields(
            payload,
            ("id", "name", "status"),
        )

    assert "name" in str(error.value)
    assert "status" in str(error.value)


def test_assert_success_response_returns_body():
    response = make_response(
        201,
        {
            "id": 1,
            "name": "Device",
            "status": "active",
        },
    )

    body = assert_success_response(
        response,
        expected_status=201,
        required_fields=("id", "name", "status"),
    )

    assert body["id"] == 1


def test_assert_error_response_returns_body():
    response = make_response(
        422,
        {
            "detail": "Validation failed",
        },
    )

    body = assert_error_response(
        response,
        expected_status=422,
    )

    assert body["detail"] == "Validation failed"


def test_assert_matches_schema_accepts_valid_payload():
    schema = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
        },
        "additionalProperties": False,
    }

    payload = {
        "id": 1,
        "name": "Device",
    }

    assert_matches_schema(payload, schema)


def test_assert_matches_schema_reports_invalid_payload():
    schema = {
        "type": "object",
        "required": ["id"],
        "properties": {
            "id": {"type": "integer"},
        },
        "additionalProperties": False,
    }

    payload = {
        "id": "not-an-integer",
    }

    with pytest.raises(AssertionError) as error:
        assert_matches_schema(payload, schema)

    message = str(error.value)

    assert "does not match" in message
    assert "not of type" in message