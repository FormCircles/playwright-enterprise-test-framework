from __future__ import annotations

import pytest

from core.assertions.api_assertions import (
    assert_error_response,
    assert_matches_schema,
    assert_status_code,
    assert_success_response,
)

from core.schemas.device_schemas import (
    DEVICE_DETAIL_SCHEMA,
    DEVICE_LIST_SCHEMA,
)

from core.test_data import InvalidDeviceFactory

pytestmark = [
    pytest.mark.api,
    pytest.mark.regression,
]


def test_get_devices_returns_list(devices_service):
    response = devices_service.get_devices()

    assert_status_code(response, 200)

    devices = response.json()
    assert_matches_schema(devices, DEVICE_LIST_SCHEMA)


def test_create_device(
    devices_service,
    device_factory,
    device_cleanup,
):
    payload = device_factory()

    response = devices_service.create_device(payload)

    created_device = assert_success_response(
        response,
        expected_status=201,
        required_fields=("id", "name", "status"),
    )

    device_cleanup(created_device)

    assert_matches_schema(
        created_device,
        DEVICE_DETAIL_SCHEMA,
    )

    assert created_device["name"] == payload["name"]
    assert created_device["status"] == payload["status"]


def test_get_device_by_id(devices_service, created_device):
    device_id = created_device["id"]

    response = devices_service.get_device_by_id(device_id)

    retrieved_device = assert_success_response(
        response,
        expected_status=200,
        required_fields=("id", "name", "status"),
    )

    assert_matches_schema(
        retrieved_device,
        DEVICE_DETAIL_SCHEMA,
    )

    assert retrieved_device["id"] == device_id
    assert retrieved_device["name"] == created_device["name"]


def test_update_device(
    devices_service,
    created_device,
    device_factory,
):
    device_id = created_device["id"]
    update_payload = device_factory(status="inactive")

    response = devices_service.update_device(
        device_id,
        update_payload,
    )

    updated_device = assert_success_response(
        response,
        expected_status=200,
        required_fields=("id", "name", "status"),
    )

    assert_matches_schema(
        updated_device,
        DEVICE_DETAIL_SCHEMA,
    )

    assert updated_device["id"] == device_id
    assert updated_device["name"] == update_payload["name"]
    assert updated_device["status"] == update_payload["status"]


def test_create_device_without_name_returns_validation_error(
    devices_service,
    device_factory,
):
    payload = InvalidDeviceFactory.missing_name()

    response = devices_service.create_device(payload)

    error_body = assert_error_response(
        response,
        expected_status=422,
    )

    assert error_body["detail"]


'''
def test_create_device_with_invalid_status_returns_validation_error(
    devices_service,
    device_factory,
):
    payload = InvalidDeviceFactory.missing_status()

    response = devices_service.create_device(payload)

    assert response.status == 422


def test_create_device_with_empty_name(
    devices_service,
    device_factory,
):
    payload = device_factory(name="")

    response = devices_service.create_device(payload)

    assert response.status == 422
'''


def test_delete_device(devices_service, created_device):
    device_id = created_device["id"]

    delete_response = devices_service.delete_device(device_id)

    assert_status_code(delete_response, 204)

    get_response = devices_service.get_device_by_id(device_id)

    assert_error_response(
        get_response,
        expected_status=404,
    )