from __future__ import annotations


class TestAdminService:
    """Administrative operations available only in test environments."""

    def __init__(self, api_client) -> None:
        self.api_client = api_client

    def reset_test_data(self):
        """Request that the backend reset its test data."""

        return self.api_client.post("/test/reset")