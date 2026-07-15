from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CleanupAction:
    """A registered cleanup operation."""

    description: str
    callback: Callable[[], Any]


class CleanupRegistry:
    """Track and execute cleanup operations after test completion."""

    def __init__(self) -> None:
        self._actions: list[CleanupAction] = []

    def register(
        self,
        callback: Callable[[], Any],
        *,
        description: str,
    ) -> None:
        """Register a cleanup callback."""

        self._actions.append(
            CleanupAction(
                description=description,
                callback=callback,
            )
        )

    def execute(self) -> None:
        """Execute registered cleanup actions in reverse order."""

        failures: list[str] = []

        for action in reversed(self._actions):
            try:
                action.callback()
            except Exception as error:
                failures.append(
                    f"{action.description}: "
                    f"{type(error).__name__}: {error}"
                )

        self._actions.clear()

        if failures:
            raise AssertionError(
                "One or more cleanup operations failed:\n"
                + "\n".join(failures)
            )

    def __len__(self) -> int:
        return len(self._actions)