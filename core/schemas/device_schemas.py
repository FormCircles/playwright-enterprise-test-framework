from __future__ import annotations

from typing import Any


DEVICE_DETAIL_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "DeviceDetailResponse",
    "type": "object",
    "required": [
        "id",
        "name",
        "status",
    ],
    "properties": {
        "id": {
            "type": "integer",
            "minimum": 1,
        },
        "name": {
            "type": "string",
        },
        "status": {
            "type": "string",
        },
    },
    "additionalProperties": False,
}


DEVICE_LIST_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "DeviceListResponse",
    "type": "array",
    "items": DEVICE_DETAIL_SCHEMA,
}