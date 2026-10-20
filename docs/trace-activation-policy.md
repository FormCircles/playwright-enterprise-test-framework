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
