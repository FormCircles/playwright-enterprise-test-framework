from __future__ import annotations

from collections.abc import Callable
from time import perf_counter
from typing import Any, Optional, TypeVar

from core.logging.api_request_logger import (
    APIRequestLogEntry,
    log_api_request,
)


ResponseT = TypeVar("ResponseT")


class APIClient:
    def __init__(
        self,
        request_context,
        auth_token: Optional[str] = None,
    ) -> None:
        self.request_context = request_context
        self.auth_token = auth_token

    def _headers(
        self,
        extra_headers: Optional[dict[str, str]] = None,
    ) -> dict[str, str]:
        headers: dict[str, str] = {}

        if self.auth_token:
            headers["Authorization"] = (
                f"Bearer {self.auth_token}"
            )

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def _execute_request(
        self,
        *,
        method: str,
        path: str,
        operation: Callable[[], ResponseT],
    ) -> ResponseT:
        started_at = perf_counter()

        response = operation()

        duration_ms = (perf_counter() - started_at) * 1000

        log_api_request(
            APIRequestLogEntry(
                method=method,
                url=path,
                status=response.status,
                duration_ms=duration_ms,
            )
        )

        return response

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ):
        return self._execute_request(
            method="GET",
            path=path,
            operation=lambda: self.request_context.get(
                path,
                params=params,
                headers=self._headers(),
            ),
        )

    def post(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
    ):
        return self._execute_request(
            method="POST",
            path=path,
            operation=lambda: self.request_context.post(
                path,
                data=data,
                headers=self._headers(),
            ),
        )

    def put(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
    ):
        return self._execute_request(
            method="PUT",
            path=path,
            operation=lambda: self.request_context.put(
                path,
                data=data,
                headers=self._headers(),
            ),
        )

    def patch(
        self,
        path: str,
        data: Optional[dict[str, Any]] = None,
    ):
        return self._execute_request(
            method="PATCH",
            path=path,
            operation=lambda: self.request_context.patch(
                path,
                data=data,
                headers=self._headers(),
            ),
        )

    def delete(self, path: str):
        return self._execute_request(
            method="DELETE",
            path=path,
            operation=lambda: self.request_context.delete(
                path,
                headers=self._headers(),
            ),
        )

    def set_auth_token(self, auth_token: str) -> None:
        self.auth_token = auth_token

    def clear_auth_token(self) -> None:
        self.auth_token = None