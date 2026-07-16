from __future__ import annotations


PROTECTED_ENVIRONMENTS = {
    "prod",
    "production",
}


def is_reset_allowed(environment: str) -> bool:
    """Return whether destructive test reset operations are allowed."""

    normalized_environment = environment.strip().lower()
    return normalized_environment not in PROTECTED_ENVIRONMENTS


def assert_reset_allowed(environment: str) -> None:
    """Prevent backend reset operations in protected environments."""

    if not is_reset_allowed(environment):
        raise RuntimeError(
            "Backend test-data reset is forbidden in "
            f"environment '{environment}'."
        )