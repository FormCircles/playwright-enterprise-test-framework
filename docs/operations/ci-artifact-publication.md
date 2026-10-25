# PETF CI Artifact Publication — Q4-S1 Checkpoint

## Scope

This document describes the implemented v1.1 checkpoint behavior, not a
v1.1.0 release. Workflows: `.github/workflows/tests.yml`,
`container-publish.yml`, and `container-run.yml`.

## Source outputs and staging

Tests write HTML/JUnit reports and diagnostics under `test-results/`.
`scripts.collect_ci_artifacts` copies **available** reports and legacy
outputs to a fresh `artifacts/<run-id>/` staging directory, with `reports/`,
`metadata/`, and an optional `legacy/` subtree. It can also stage the FastAPI
server log. It does not generate missing reports or alter source artifacts.
The workflow supplies a run ID and receives `artifact_path` through
`GITHUB_OUTPUT` after successful collection.

Example (use a unique run ID and a disposable workspace when testing):

```bash
python -m scripts.collect_ci_artifacts --run-id local-verification
```

## Security gate and publication

The collector calls `verify_artifact_security` on staged content. On failure,
it deletes the new staging directory and raises an error; upload must not
proceed. All three workflows gate `actions/upload-artifact@v4` on successful
collection and non-cancellation. Collection is configured to allow verified
failure evidence after test failures, provided the job is not cancelled.
The container-publish workflow additionally requires a `main` push and
successful artifact collection before publishing the tested image to GHCR.
Container workflow artifact retention is configured for 14 days; consult
each workflow for its exact upload name and settings.

Console diagnostic text uses `scripts.safe_console_log` where configured;
unsafe content is withheld rather than printed. Other commands' output is
not automatically covered by this helper.

## Limits and troubleshooting

Security scanning is pattern-based and cannot detect every secret.
Screenshot image contents are **not** scanned; traces can contain sensitive
application/network information. Restrict artifact access and apply suitable
retention and review practices.

If upload is skipped, inspect the collection/security step before changing
the upload condition. If a report is missing, verify the test command created
it under `test-results/`. If security verification fails, correct the source
of sensitive output; **do not bypass the gate**. If container image publication
is skipped, check both the `main` push condition and successful collection.

## Related documentation

- [Configuration and environments](../testing/base-url-resolution.md)
- [Artifact directory contract](../architecture/artifact-directory-contract.md)
- [Screenshot hygiene](../screenshot-artifact-hygiene.md)
- [Trace activation](../trace-activation-policy.md)
- [PETF-102 security review](../verification/PETF-102-artifact-publication-security.md)
