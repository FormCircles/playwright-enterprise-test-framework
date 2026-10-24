# PETF-97 — Artifact Behavior Verification

## Objective

Verify serial, parallel, and failed-run artifact behavior,
including completeness, collision resistance, cleanup,
retention, and protection against recognizable credentials.

## Implementation

PETF-97 extends the artifact publication foundation
established by PETF-95 and PETF-96.

Changes include:

- Pre-publication artifact security verification.
- Inspection of supported text files and ZIP archives.
- Detection of selected credential patterns.
- Rejection of malformed and unsupported artifacts.
- Removal of rejected publication staging directories.
- Preservation of original test evidence.
- CI upload gating on successful collection.

## Verification Results

| Scenario | Result |
|---|---|
| Serial collection isolation | PASS |
| Eight concurrent collector invocations | PASS |
| Collision resistance | PASS |
| Failed-run evidence preservation | PASS |
| Original evidence preservation | PASS |
| Direct credential rejection | PASS |
| Nested ZIP credential rejection | PASS |
| Rejected staging cleanup | PASS |
| Temporary verification workspace cleanup | PASS |
| Security and collector regression | PASS: 20 tests |
| Remaining diagnostics regression | PASS: 69 tests, 1 skipped |
| Ruff | PASS |
| mypy | PASS |
| CI workflow configuration | PASS |
| CI artifact retention configuration | PASS: 14 days |

## Security Limitations

The scanner rejects recognized credentials in supported
text files and ZIP archive contents.

It does not guarantee detection of every secret.

Known limitations include:

- Encoded or obfuscated credentials may escape detection.
- Images are not inspected for sensitive visual content.
- Detection depends on supported credential patterns.
- Unsupported artifact formats are rejected.
- File size and archive inspection limits apply.

Artifact producers must avoid writing sensitive information
to screenshots, traces, reports, and logs.

## Verification Boundaries

The following remain unverified:

1. Actual parallel pytest-xdist or Playwright worker execution.
2. Artifact contents uploaded by GitHub Actions.
3. Artifact upload after a failing CI test.
4. Actual expiration after the configured 14-day retention period.

Eight concurrent collector calls were verified, but this is
not equivalent to actual parallel test-worker execution.

The 14-day retention configuration was validated, but
expiration cannot be confirmed without observing the
artifact lifecycle.

## Closure Criteria

Before closing PETF-97:

- Validate the PR's GitHub Actions execution.
- Inspect at least one uploaded CI artifact.
- Confirm failure-path upload behavior or record an
  explicit follow-up.
- Record decisions for remaining verification boundaries.

## Local Verification Environment

Ubuntu VM with 15 GiB RAM and 4 GiB swap.

The full non-integration regression suite was not
completed during final validation because repeated shell
crashes occurred during attempts to run the larger batch.

Focused diagnostics regression and static quality checks
passed independently.
