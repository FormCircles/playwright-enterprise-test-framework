# Test Data Naming Conventions

## Purpose

This document defines the naming conventions used for automation-created test data within the Playwright Enterprise Test Framework.

Following a consistent naming convention makes it easier to:

- Identify automation-created records
- Distinguish test data from manually created data
- Simplify debugging and troubleshooting
- Support automated cleanup
- Maintain consistency across API, UI, and integration tests

---

# Standard Naming Format

Automation-created records should follow the format:

```
AUTO-<RESOURCE>-<UNIQUE_ID>
```

Examples:

```
AUTO-DEVICE-a1b2c3d4
AUTO-USER-f9e8d7c6
AUTO-ACCOUNT-98ab12cd
AUTO-ORDER-1234abcd
```

---

# Device Test Data

Device payloads created by the framework should use:

```
AUTO-DEVICE-<UNIQUE_ID>
```

Example:

```json
{
    "name": "AUTO-DEVICE-a1b2c3d4",
    "status": "online"
}
```

The unique identifier should be generated dynamically using a UUID.

Example:

```python
from uuid import uuid4

name = f"AUTO-DEVICE-{uuid4().hex[:8]}"
```

---

# Request vs Response

Device payload factories generate **request payloads**.

Example request:

```json
{
    "name": "AUTO-DEVICE-a1b2c3d4",
    "status": "online"
}
```

The API is responsible for generating the device ID.

Example response:

```json
{
    "id": 3,
    "name": "AUTO-DEVICE-a1b2c3d4",
    "status": "online"
}
```

Automation factories should **not** generate IDs.

---

# Invalid Payload Naming

Invalid payloads should still use the automation prefix whenever possible.

Examples:

```
AUTO-DEVICE-invalid-status-a1b2c3d4
AUTO-DEVICE-empty-name-a1b2c3d4
AUTO-DEVICE-null-status-a1b2c3d4
```

If a test intentionally validates an empty or missing name, the name field may intentionally violate this convention.

---

# Resource Prefixes

Reserved prefixes include:

| Resource | Prefix |
|----------|--------|
| Device | AUTO-DEVICE |
| User | AUTO-USER |
| Account | AUTO-ACCOUNT |
| Order | AUTO-ORDER |
| Session | AUTO-SESSION |

Future factories should follow the same pattern.

---

# Metadata

When supported by the application, automation-created records may include metadata such as:

| Field | Description |
|--------|-------------|
| created_by | automation |
| environment | local, ci, staging |
| test_case | Test name |
| test_run_id | CI run identifier |
| created_at | Timestamp |

Only include metadata if supported by the API contract.

---

# Cleanup

Automation cleanup should use resource IDs returned by the API rather than relying on name prefixes.

Preferred:

```python
device_cleanup(created_device["id"])
```

Avoid deleting records solely based on their names.

---

# DeviceFactory Standard

`DeviceFactory` should generate payloads using the documented naming convention.

Example:

```python
from uuid import uuid4

class DeviceFactory:

    PREFIX = "AUTO-DEVICE"

    @classmethod
    def create(cls, **overrides):
        payload = {
            "name": f"{cls.PREFIX}-{uuid4().hex[:8]}",
            "status": "online",
        }

        payload.update(overrides)

        return payload
```

---

# InvalidDeviceFactory Standard

`InvalidDeviceFactory` should generate invalid payloads by starting from a valid payload created by `DeviceFactory` and modifying only the fields necessary for the specific negative test.

Example:

```python
payload = DeviceFactory.create()
payload.pop("name")
```

instead of constructing an entirely new payload.

---

# Best Practices

- Always use reusable factories to generate test data.
- Do not hardcode device names inside tests.
- Generate unique names to avoid collisions.
- Keep payload generation centralized.
- Keep pytest fixtures lightweight by delegating payload creation to reusable factories.
- Use server-generated IDs returned by the API.
- Keep test data deterministic and easy to identify.

---

# Summary

The standard naming convention for automation-created records is:

```
AUTO-<RESOURCE>-<UNIQUE_ID>
```

Examples:

```
AUTO-DEVICE-a1b2c3d4
AUTO-USER-6f5e4d3c
AUTO-ACCOUNT-1234abcd
```

This convention provides consistency across the Playwright Enterprise Test Framework and serves as the foundation for future dynamic test data factories.