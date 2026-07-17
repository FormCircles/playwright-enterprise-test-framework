from __future__ import annotations

import logging

from core.api.api_client import APIClient


class FakeResponse:
    status = 200


class FakeRequestContext:
    def get(self, path, params=None, headers=None):
        return FakeResponse()


def test_api_client_logs_completed_get_request(caplog) -> None:
    caplog.set_level(logging.INFO)

    client = APIClient(FakeRequestContext())

    response = client.get("/health")

    assert response.status == 200
    assert "method=GET" in caplog.text
    assert "url=/health" in caplog.text
    assert "status=200" in caplog.text
    assert "duration_ms=" in caplog.text