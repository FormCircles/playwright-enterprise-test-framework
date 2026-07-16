"""Environment safety utilities."""

from core.environment.environment_guard import (
    assert_reset_allowed,
    is_reset_allowed,
)

__all__ = [
    "assert_reset_allowed",
    "is_reset_allowed",
]