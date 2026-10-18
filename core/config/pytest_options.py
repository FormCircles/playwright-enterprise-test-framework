"""Shared pytest configuration option helpers."""

from __future__ import annotations

import os
import shlex


def explicit_base_url(pytestconfig) -> str | None:
    """Return BASE_URL explicitly supplied through pytest options."""

    invocation_args = list(pytestconfig.invocation_params.args)
    addopts_args = shlex.split(os.environ.get("PYTEST_ADDOPTS", ""))

    def count_options(arguments: list[str]) -> int:
        count = 0

        for index, argument in enumerate(arguments):
            if argument == "--base-url":
                if index + 1 >= len(arguments):
                    raise ValueError("--base-url requires a value.")
                count += 1
            elif argument.startswith("--base-url="):
                count += 1

        return count

    occurrences = (
        count_options(invocation_args)
        + count_options(addopts_args)
    )

    if occurrences == 0:
        return None

    return pytestconfig.getoption("--base-url")
