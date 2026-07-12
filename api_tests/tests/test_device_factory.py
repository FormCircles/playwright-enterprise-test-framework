from __future__ import annotations


def test_device_factory_creates_valid_payload(device_factory):
    payload = device_factory()

    assert "name" in payload
    assert payload["name"].startswith("Test Device ")
    assert payload["status"] == "active"


def test_device_factory_creates_unique_names(device_factory):
    first_payload = device_factory()
    second_payload = device_factory()

    assert first_payload["name"] != second_payload["name"]


def test_device_factory_supports_overrides(device_factory):
    payload = device_factory(
        name="Custom Device",
        status="inactive",
    )

    assert payload["name"] == "Custom Device"
    assert payload["status"] == "inactive"