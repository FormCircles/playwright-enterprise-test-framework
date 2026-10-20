"""PETF Playwright trace activation policy."""

TRACE_MODES = ("off", "on-failure")

NATIVE_TRACE_MODES = {
    "off": "off",
    "on-failure": "retain-on-failure",
}


def resolve_trace_mode(mode: str) -> str:
    """Translate a PETF trace mode to pytest-playwright."""
    if mode not in NATIVE_TRACE_MODES:
        raise ValueError(f"Unsupported PETF trace mode: {mode}")
    return NATIVE_TRACE_MODES[mode]
