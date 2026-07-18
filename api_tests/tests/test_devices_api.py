from __future__ import annotations

import pytest


pytestmark = [
    pytest.mark.api,
    pytest.mark.regression,
]


def test_create_device_with_missing_status_returns_422(devices_service):
    invalid_payload = {
        "name": "Broken Device",
    }

    response = devices_service.create_device(invalid_payload)

    assert response.status == 422, (
        f"Expected 422 for an invalid device payload, "
        f"got {response.status}. Body: {response.text()}"
    )


def test_get_nonexistent_device_returns_404(devices_service):
    response = devices_service.get_device_by_id(999999)

    assert response.status == 404, (
        f"Expected 404 for a nonexistent device, "
        f"got {response.status}. Body: {response.text()}"
    )


def test_delete_nonexistent_device_returns_404(devices_service):
    response = devices_service.delete_device(999999)

    assert response.status == 404, (
        f"Expected 404 when deleting a nonexistent device, "
        f"got {response.status}. Body: {response.text()}"
    )