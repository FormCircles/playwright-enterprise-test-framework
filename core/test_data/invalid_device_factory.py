from __future__ import annotations

from typing import Any

from core.test_data.device_factory import DeviceFactory


class InvalidDeviceFactory:
    """Generate invalid device payloads for negative API testing."""

    @staticmethod
    def missing_name() -> dict[str, Any]:
        payload = DeviceFactory.create()
        payload.pop("name")
        return payload

    @staticmethod
    def empty_name() -> dict[str, Any]:
        return DeviceFactory.create(
            name=""
        )

    @staticmethod
    def null_name() -> dict[str, Any]:
        payload = DeviceFactory.create()
        payload["name"] = None
        return payload

    @staticmethod
    def invalid_status() -> dict[str, Any]:
        return DeviceFactory.create(
            status="unsupported"
        )

    @staticmethod
    def numeric_status() -> dict[str, Any]:
        payload = DeviceFactory.create()
        payload["status"] = 123
        return payload

    @staticmethod
    def missing_status() -> dict[str, Any]:
        payload = DeviceFactory.create()
        payload.pop("status")
        return payload