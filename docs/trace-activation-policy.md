# PETF Trace Activation Policy

## Purpose
PETF provides configurable Playwright trace activation.
Tracing is disabled by default to reduce resource consumption.

## Supported Policies
- off: Disable tracing (default).
- on-failure: Retain traces for failed tests.

## Usage
Run UI tests with --petf-trace=on-failure.
Native --tracing=retain-on-failure is also supported.
Do not specify both options together.

## Retry Support
Retry-specific tracing is not implemented in PETF-86.

## Retention and Security
PETF-86 does not enforce artifact count, size, or expiration limits.
Traces may contain sensitive application and network information.
Restrict artifact access and apply retention controls.

## PETF v1.1 Trace Operations

Tracing defaults to `off`. For PETF-managed failure-only retention, run:

```bash
pytest --env=local --petf-trace=on-failure
```

This mode activates native tracing and, after the teardown report, removes
`trace*.zip` for tests without a failure in any phase. Failed tests retain
traces. Native pytest-playwright `--tracing=retain-on-failure` is also
supported, but do not supply native `--tracing` and `--petf-trace` together.
The UI `output_path` fixture reserves per-test paths under
`test-results/playwright/`. Retry-specific PETF policies, age-based cleanup,
and size quotas are not implemented. Trace archives can contain sensitive
application and network data; they are not guaranteed to be redacted.
See [CI publication operations](operations/ci-artifact-publication.md).
