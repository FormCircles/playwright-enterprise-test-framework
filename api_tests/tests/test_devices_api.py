def test_create_device_invalid_payload(devices_service):
    payload = {
        "name": "Broken Device"
        # missing "status"
    }

    response = devices_service.create_device(payload)

    assert response.status == 422


def test_get_nonexistent_device(devices_service):
    response = devices_service.get_device_by_id(999999)

    assert response.status == 404


def test_delete_nonexistent_device(devices_service):
    response = devices_service.delete_device(999999)

    assert response.status == 404


def test_get_devices_returns_list(devices_service):
    response = devices_service.get_devices()

    assert response.status == 200
    assert isinstance(response.json(), list)


def test_create_device(devices_service):
    payload = {
        "name": "New Device",
        "status": "offline",
    }

    response = devices_service.create_device(payload)

    assert response.status == 201
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["status"] == payload["status"]


def test_get_device_by_id(devices_service, created_device):
    device_id = created_device["id"]

    response = devices_service.get_device_by_id(device_id)

    assert response.status == 200
    assert response.json()["id"] == device_id


def test_update_device(devices_service, created_device):
    device_id = created_device["id"]

    payload = {
        "name": "Updated Device",
        "status": "online",
    }

    response = devices_service.update_device(device_id, payload)

    assert response.status == 200
    assert response.json()["name"] == "Updated Device"


def test_delete_device(devices_service, created_device):
    device_id = created_device["id"]

    response = devices_service.delete_device(device_id)

    assert response.status == 204