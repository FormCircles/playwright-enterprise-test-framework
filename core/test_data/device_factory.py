from __future__ import annotations

from typing import Any
from uuid import uuid4


class DeviceFactory:
    """Generate valid and reusable device request payloads."""

    @staticmethod
    def create(**overrides: Any) -> dict[str, Any]:
        """Create a valid device payload with optional overrides."""

        payload: dict[str, Any] = {
            "name": f"Test Device {uuid4().hex[:8]}",
            "status": "active",
        }

        payload.update(overrides)
        return payload