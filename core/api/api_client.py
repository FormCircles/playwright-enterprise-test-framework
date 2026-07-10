from __future__ import annotations

from typing import Any, Optional


class APIClient:
    def __init__(self, request_context, auth_token: Optional[str] = None) -> None:
        self.request_context = request_context
        self.auth_token = auth_token

    def _headers(self, extra_headers: Optional[dict[str, str]] = None) -> dict[str, str]:
        headers: dict[str, str] = {}

        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def get(self, path: str, params: Optional[dict[str, Any]] = None):
        return self.request_context.get(
            path,
            params=params,
            headers=self._headers(),
        )

    def post(self, path: str, data: Optional[dict[str, Any]] = None):
        return self.request_context.post(
            path,
            data=data,
            headers=self._headers(),
        )

    def put(self, path: str, data: Optional[dict[str, Any]] = None):
        return self.request_context.put(
            path,
            data=data,
            headers=self._headers(),
        )

    def delete(self, path: str):
        return self.request_context.delete(
            path,
            headers=self._headers(),
        )

    def set_auth_token(self, auth_token: str) -> None:
        self.auth_token = auth_token

    def clear_auth_token(self) -> None:
        self.auth_token = None

    def patch(self, path: str, data: Optional[dict[str, Any]] = None):
        return self.request_context.patch(
            path,
            data=data,
            headers=self._headers(),
        )