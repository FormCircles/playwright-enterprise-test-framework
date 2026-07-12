from __future__ import annotations

import pytest


def test_get_devices_returns_list(devices_service):
    response = devices_service.get_devices()

    assert response.status == 200, (
        f"Expected 200 when listing devices, got {response.status}. "
        f"Body: {response.text()}"
    )

    devices = response.json()
    assert isinstance(devices, list), (
        f"Expected device collection to be a list, got: {devices}"
    )


@pytest.mark.regression
@pytest.mark.api
def test_create_device(devices_service, device_factory):
    payload = device_factory()

    response = devices_service.create_device(payload)

    assert response.status == 201, (
        f"Expected 201 when creating device, got {response.status}. "
        f"Body: {response.text()}"
    )

    created_device = response.json()

    assert "id" in created_device
    assert created_device["name"] == payload["name"]
    assert created_device["status"] == payload["status"]


def test_get_device_by_id(devices_service, created_device):
    device_id = created_device["id"]

    response = devices_service.get_device_by_id(device_id)

    assert response.status == 200, (
        f"Expected 200 when retrieving device {device_id}, "
        f"got {response.status}. Body: {response.text()}"
    )

    retrieved_device = response.json()

    assert retrieved_device["id"] == device_id
    assert retrieved_device["name"] == created_device["name"]


def test_update_device(devices_service, created_device, device_factory):
    device_id = created_device["id"]
    update_payload = device_factory(status="inactive")

    response = devices_service.update_device(device_id, update_payload)

    assert response.status == 200, (
        f"Expected 200 when updating device {device_id}, "
        f"got {response.status}. Body: {response.text()}"
    )

    updated_device = response.json()

    assert updated_device["id"] == device_id
    assert updated_device["name"] == update_payload["name"]
    assert updated_device["status"] == update_payload["status"]


def test_create_device_without_name_returns_validation_error(
    devices_service,
    device_factory,
):
    payload = device_factory()
    payload.pop("name")

    response = devices_service.create_device(payload)

    assert response.status == 422


'''
def test_create_device_with_invalid_status_returns_validation_error(
    devices_service,
    device_factory,
):
    payload = device_factory(status="unsupported")

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

    assert delete_response.status == 204, (
        f"Expected 204 when deleting device {device_id}, "
        f"got {delete_response.status}. Body: {delete_response.text()}"
    )

    get_response = devices_service.get_device_by_id(device_id)
    assert get_response.status == 404, (
        f"Expected deleted device {device_id} to return 404, "
        f"got {get_response.status}."
    )