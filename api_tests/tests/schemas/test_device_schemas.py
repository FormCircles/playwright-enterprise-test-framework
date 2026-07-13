from __future__ import annotations

from core.schemas.device_schemas import (
    DEVICE_DETAIL_SCHEMA,
    DEVICE_LIST_SCHEMA,
)


def test_device_detail_schema_defines_expected_required_fields():
    assert DEVICE_DETAIL_SCHEMA["type"] == "object"
    assert set(DEVICE_DETAIL_SCHEMA["required"]) == {
        "id",
        "name",
        "status",
    }


def test_device_detail_schema_rejects_additional_properties():
    assert DEVICE_DETAIL_SCHEMA["additionalProperties"] is False


def test_device_list_schema_uses_device_detail_schema():
    assert DEVICE_LIST_SCHEMA["type"] == "array"
    assert DEVICE_LIST_SCHEMA["items"] is DEVICE_DETAIL_SCHEMA