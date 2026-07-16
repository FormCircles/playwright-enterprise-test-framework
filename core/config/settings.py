from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


CONFIG_FILE = Path(__file__).resolve().parent / "environments.yaml"


class Settings:
    """Load environment-specific test configuration."""

    def __init__(self, env: str = "local") -> None:
        environments = self._load_environments()

        if env not in environments:
            available_environments = ", ".join(sorted(environments))
            raise ValueError(
                f"Unknown environment: {env}. "
                f"Available environments: {available_environments}"
            )

        environment_config = environments[env]

        self.env = env

        self.base_url = os.getenv(
            "BASE_URL",
            self._require_string(environment_config, "base_url"),
        )

        self.username = os.getenv(
            "TEST_USERNAME",
            self._require_string(environment_config, "username"),
        )

        self.password = os.getenv("TEST_PASSWORD", "")

        self.request_timeout_ms = self._positive_integer(
            environment_config,
            "request_timeout_ms",
            default=30_000,
        )

        self.ui_timeout_ms = self._positive_integer(
            environment_config,
            "ui_timeout_ms",
            default=30_000,
        )

        self.headless = self._boolean(
            environment_config,
            "headless",
            default=True,
        )

    @staticmethod
    def _load_environments() -> dict[str, dict[str, Any]]:
        with CONFIG_FILE.open("r", encoding="utf-8") as file:
            environments = yaml.safe_load(file) or {}

        if not isinstance(environments, dict):
            raise ValueError(
                "Environment configuration must be a mapping."
            )

        return environments

    @staticmethod
    def _require_string(
        config: dict[str, Any],
        key: str,
    ) -> str:
        value = config.get(key)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Configuration value '{key}' must be a non-empty string."
            )

        return value.strip()

    @staticmethod
    def _positive_integer(
        config: dict[str, Any],
        key: str,
        *,
        default: int,
    ) -> int:
        value = config.get(key, default)

        if not isinstance(value, int) or value <= 0:
            raise ValueError(
                f"Configuration value '{key}' must be a positive integer."
            )

        return value

    @staticmethod
    def _boolean(
        config: dict[str, Any],
        key: str,
        *,
        default: bool,
    ) -> bool:
        value = config.get(key, default)

        if not isinstance(value, bool):
            raise ValueError(
                f"Configuration value '{key}' must be a boolean."
            )

        return value

    def require_password(self) -> str:
        """Return the configured password or raise a helpful error."""

        if not self.password:
            raise RuntimeError(
                "TEST_PASSWORD is required for authenticated tests."
            )

        return self.password