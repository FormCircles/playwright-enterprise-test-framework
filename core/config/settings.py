from __future__ import annotations

import os
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml


CONFIG_FILE = Path(__file__).resolve().parent / "environments.yaml"


class Settings:
    """Load environment-specific test configuration."""

    def __init__(
        self,
        env: str = "local",
        *,
        cli_overrides: dict[str, str] | None = None,
    ) -> None:
        environments = self._load_environments()

        if env not in environments:
            available_environments = ", ".join(sorted(environments))
            raise ValueError(
                f"Unknown environment: {env}. "
                f"Available environments: {available_environments}"
            )

        environment_config = environments[env]

        self.env = env
        overrides = cli_overrides or {}

        self.base_url = self._resolve_string(
            key="base_url",
            cli_value=overrides.get("base_url"),
            environment_variables=("BASE_URL", "PYTEST_BASE_URL"),
            environment_config=environment_config,
        )

        self._validate_execution_target()

        self.username = self._resolve_string(
            key="username",
            cli_value=overrides.get("username"),
            environment_variables=("TEST_USERNAME",),
            environment_config=environment_config,
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

    @classmethod
    def _resolve_string(
        cls,
        *,
        key: str,
        cli_value: str | None,
        environment_variables: tuple[str, ...],
        environment_config: dict[str, Any],
    ) -> str:
        """Resolve CLI > environment variables > environment YAML."""

        if cli_value is not None:
            value = cli_value
        else:
            value = None

            for variable in environment_variables:
                if variable in os.environ:
                    value = os.environ[variable]
                    break

            if value is None:
                value = environment_config.get(key)

        resolved = cls._require_string({key: value}, key)

        if key == "base_url":
            return cls._validate_base_url(resolved)

        return resolved

    def _validate_execution_target(self) -> None:
        """Reject unexpected targets for the CI execution environment."""

        if self.env != "ci":
            return

        approved_ci_target = "http://127.0.0.1:8080"

        if self.base_url != approved_ci_target:
            raise ValueError(
                "Unsafe CI BASE_URL: "
                f"{self.base_url!r}. "
                "The ci environment only permits "
                f"{approved_ci_target!r}."
            )

    @staticmethod
    def _validate_base_url(value: str) -> str:
        """Validate the resolved HTTP(S) application URL."""

        try:
            parsed = urlsplit(value)
            valid_port = parsed.port
        except ValueError as exc:
            raise ValueError(
                "Configuration value 'base_url' must be a valid HTTP(S) URL."
            ) from exc

        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or any(char.isspace() for char in value)
            or (valid_port is not None and valid_port <= 0)
        ):
            raise ValueError(
                "Configuration value 'base_url' must be a valid HTTP(S) URL "
                "without credentials, query parameters, or fragments."
            )

        return value

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