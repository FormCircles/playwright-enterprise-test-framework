from __future__ import annotations

from collections.abc import Callable
from typing import Any
from uuid import uuid4

import pytest


@pytest.fixture
def created_device(devices_service, device_factory):
    """Create a device for a test and clean it up afterward."""

    payload = device_factory()
    response = devices_service.create_device(payload)

    assert response.status == 201, (
        f"Failed to create device fixture. "
        f"Status: {response.status}. Body: {response.text()}"
    )

    device = response.json()

    yield device

    cleanup_response = devices_service.delete_device(device["id"])

    assert cleanup_response.status in {204, 404}, (
        f"Failed to clean up device {device['id']}. "
        f"Status: {cleanup_response.status}. "
        f"Body: {cleanup_response.text()}"
    )