from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from core.test_data.device_factory import DeviceFactory


@pytest.fixture
def device_factory() -> Callable[..., dict[str, Any]]:
    """Expose the reusable device payload factory."""

    return DeviceFactory.create


@pytest.fixture
def created_device(
    devices_service,
    device_factory,
    device_cleanup,
):
    """Create and register a reusable test device."""

    payload = device_factory()
    response = devices_service.create_device(payload)

    assert response.status == 201, (
        f"Failed to create test device. "
        f"Status: {response.status}. Body: {response.text()}"
    )

    device = response.json()
    device_cleanup(device)

    return device


@pytest.fixture
def device_cleanup(
    devices_service,
) -> Callable[[int | str | dict[str, Any]], None]:
    """Track created devices and delete them after the test."""

    device_ids: list[int | str] = []

    def _register(device: int | str | dict[str, Any]) -> None:
        if isinstance(device, dict):
            device_id = device.get("id")

            if device_id is None:
                raise ValueError(
                    "Cannot register device cleanup: device has no 'id'."
                )
        else:
            device_id = device

        device_ids.append(device_id)

    yield _register

    cleanup_failures: list[str] = []

    for device_id in reversed(device_ids):
        response = devices_service.delete_device(device_id)

        if response.status not in {204, 404}:
            cleanup_failures.append(
                f"Device {device_id}: status={response.status}, "
                f"body={response.text()}"
            )

    assert not cleanup_failures, (
        "One or more test devices could not be cleaned up:\n"
        + "\n".join(cleanup_failures)
    )
