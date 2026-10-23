# PETF Canonical Artifact Directory Contract

## Status

PETF-95 establishes the canonical artifact directory utilities.
Existing artifact producers and CI publication will be migrated
in subsequent PETF-94 subtasks.

## Directory Layout

    artifacts/
      <run-id>/
        reports/
        metadata/
        workers/
          <worker-id>/
            <suite-id>/
              <test-id>/
                logs/
                screenshots/
                traces/
                attachments/

## Identity Rules

- Run IDs identify independent executions and must be shared by
  workers participating in the same execution.
- Worker IDs isolate parallel execution. Use `main` for serial
  execution and pytest-xdist identifiers such as `gw0` for workers.
- Suite IDs distinguish API, UI, and other test families.
- Test IDs are deterministic SHA-256-derived identifiers generated
  from complete pytest node IDs, including parameterization.
- Callers supply run, worker, suite, and test identities.

## Directory Ownership

- Reports and metadata belong to the run.
- Worker directories isolate concurrent workers.
- Test directories isolate individual test identities.
- Logs, screenshots, traces, and attachments belong to tests.

## Directory Creation and Collision Handling

`ensure_artifact_directory()` creates directories idempotently.

`reserve_artifact_directory()` atomically reserves distinct
directories, preserving earlier artifacts when paths collide.

Directory creation alone does not prevent file overwrites.
Artifact producers must use exclusive reservations or equivalent
safe-write mechanisms when repeated writes are possible.

## Path Safety

PETF reuses its existing collision-resistant path sanitization.
Test node IDs are hashed into opaque directory components.

The artifact root is trusted caller-supplied configuration.

## Compatibility

PETF-95 does not migrate existing artifact producers.

Current locations include:

- `test-results/playwright/`
- `test-results/screenshots/`
- `test-results/diagnostics/`
- `test-results/` for CI reports

Subsequent PETF-94 work will migrate producers and CI workflows
while preserving existing trace retention, screenshot handling,
failure diagnostics, and parallel isolation behavior.

## Verification

Regression coverage:
`api_tests/tests/diagnostics/test_artifact_paths.py`

The tests verify deterministic paths, identity isolation,
parameterized tests, supported artifact kinds, directory creation,
exclusive reservation, path safety, and shared report locations.
