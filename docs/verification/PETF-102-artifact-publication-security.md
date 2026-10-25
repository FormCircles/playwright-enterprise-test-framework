# PETF-102 — Configuration Logs and Artifact Security Review

## Objective

Review PETF configuration logs, test evidence, and CI artifact
publication for security regressions.

## Findings

### SEC-01 — Missing artifact publication security gates

The container-publish and container-run workflows previously uploaded
test-results directly without canonical pre-publication verification.

Remediation:
- Reuse scripts.collect_ci_artifacts.
- Require successful collection before artifact upload.
- Preserve smoke reports and container diagnostic logs.
- Execute collection after test failures when not cancelled.

### SEC-02 — Inconsistent artifact retention

Container workflows did not explicitly enforce the existing
14-day artifact retention policy.

Remediation:
- Set retention-days: 14.
- Set if-no-files-found: error.

### SEC-03 — Unverified console-log output

Workflows printed application and container logs directly to
GitHub Actions consoles.

Remediation:
- Add scripts.safe_console_log.
- Verify recognizable credentials before displaying logs.
- Withhold unsafe diagnostic content.
- Preserve container failure diagnostics.
- Use a public text-content security verification interface.

## Verification Evidence

- Configuration and artifact security regression tests: 71 passed.
- Focused artifact collector and console-log tests: 29 passed.
- Three GitHub Actions workflow files parsed successfully.
- Workflow collector execution conditions validated.
- Ruff checks passed.
- Git whitespace validation passed.

Earlier PETF-102 investigation also completed three overlapping
security test batches totaling 137 successful test executions.

## Security Limitations

- Credential detection is pattern-based and cannot detect every secret.
- Screenshot contents are not inspected for embedded secrets.
- GitHub Actions runtime behavior requires PR CI verification.
- Console logs emitted by other commands remain outside this utility.
- Container image publication must be verified in GitHub-hosted CI.

## Release Status

Local implementation and focused verification complete.

GitHub Actions CI verification: Pending.
Pull request review and merge: Pending.
