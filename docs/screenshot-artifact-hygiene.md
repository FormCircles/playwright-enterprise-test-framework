# Screenshot Artifact Hygiene

## Purpose

PETF captures screenshots for eligible failed UI tests to support
failure investigation.

## Artifact layout

Screenshots are stored under:

`test-results/screenshots/<run-id>/<worker-id>/<test-hash>.png`

The filename uses a truncated SHA-256 digest of the pytest node ID.

This provides deterministic identification without exposing readable
test names or parameter values in filenames.

SHA-256 hashing is not encryption. Predictable identifiers may be
susceptible to guessing.

## Parallel execution

Run and worker identifiers isolate screenshots produced by different
pytest executions and pytest-xdist workers.

Repeated captures use exclusive file creation and numeric suffixes
to avoid overwriting existing evidence.

## Capture failures

Screenshot capture errors do not propagate into the original pytest
failure.

Incomplete screenshot files are removed when possible.

If filesystem cleanup fails, PETF logs a warning and preserves the
original test outcome. An incomplete artifact may remain.

## Sensitive information

PETF does not automatically redact screenshot image contents.

Screenshots may contain passwords, tokens, personal information,
or other sensitive browser content.

Test authors should avoid displaying secrets in captured UI states.

Access to screenshot artifacts should be restricted to authorized
users. Artifact storage, sharing, and retention policies must reflect
the sensitivity of the captured information.

Other pytest reports and diagnostic output may contain readable
test identifiers or sensitive values.

## Retention

PETF does not intentionally delete successful screenshots when a
subsequent run starts.

Separate runs use distinct run directories.

Local artifact retention depends on filesystem availability and
external cleanup policies.

CI artifact availability and expiration depend on the configured
CI platform and upload settings.

PETF does not currently implement automatic age-based screenshot
retention or deletion.

## Verification

Regression tests cover:

- Eligible screenshot capture
- Missing and closed browser pages
- Capture and storage failures
- Partial screenshot cleanup
- Cleanup failure isolation
- Duplicate screenshot protection
- Deterministic worker-safe paths
- Opaque filenames
- Cross-run and cross-process retention

Parallel pytest-xdist regression execution verifies compatibility
with multiple workers. It does not, by itself, prove simultaneous
real-browser screenshot capture.
