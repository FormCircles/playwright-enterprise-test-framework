from __future__ import annotations

from core.test_data.device_factory import DeviceFactory


def test_device_factory_creates_valid_payload():
    payload = DeviceFactory.create()

    assert payload["name"].startswith("Test Device ")
    assert payload["status"] == "active"
    assert set(payload) == {"name", "status"}


def test_device_factory_creates_unique_names():
    first_payload = DeviceFactory.create()
    second_payload = DeviceFactory.create()

    assert first_payload["name"] != second_payload["name"]


def test_device_factory_supports_overrides():
    payload = DeviceFactory.create(
        name="Custom Device",
        status="inactive",
    )

    assert payload == {
        "name": "Custom Device",
        "status": "inactive",
    }


def test_device_factory_does_not_add_client_generated_id():
    payload = DeviceFactory.create()

    assert "id" not in payload