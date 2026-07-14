from core.test_data import InvalidDeviceFactory


def test_missing_name():
    payload = InvalidDeviceFactory.missing_name()

    assert "name" not in payload


def test_empty_name():
    payload = InvalidDeviceFactory.empty_name()

    assert payload["name"] == ""


def test_null_name():
    payload = InvalidDeviceFactory.null_name()

    assert payload["name"] is None


def test_invalid_status():
    payload = InvalidDeviceFactory.invalid_status()

    assert payload["status"] == "unsupported"


def test_numeric_status():
    payload = InvalidDeviceFactory.numeric_status()

    assert payload["status"] == 123


def test_missing_status():
    payload = InvalidDeviceFactory.missing_status()

    assert "status" not in payload