# PETF-91 — Reference-SUT boundary assessment

**Status:** Inventory classified at evidence-row level; implementation deferred to PETF-90.
**Source:** 88 tracked source/config files; 536 static evidence rows.
**Scope:** Static inventory plus direct review of root `conftest.py`, API/data/UI fixtures, device factory, settings, environment YAML, and workflow reference matches.

## Architectural rule

`core/` supplies generic configuration, Playwright clients, fixtures, diagnostics, assertions, and cleanup primitives. Reference SUT services, page objects, API routes, schemas, device payloads, and test lifecycle belong to consumer-owned code. Consumers may import `core`; `core` must not import consumer modules. CI may deliberately exercise the reference SUT.

## Inventory disposition

The accompanying CSV preserves all 536 original evidence rows and adds `final_classification`, `disposition`, and `review_basis` columns. These are **evidence-row classifications, not counts of unique defects**. Generic Python imports and keyword hits are not defects. Classifications marked static/path-based are triage judgments rather than proof that the entire file was manually audited.

| Classification | Evidence rows |
|---|---:|
| Generic framework mechanism | 106 |
| Intentional reference validation | 345 |
| Needs targeted review | 22 |
| Prohibited core coupling | 55 |
| Prohibited public-boundary coupling | 8 |

## Confirmed prohibited boundaries

| Location | Evidence | Proposed disposition |
|---|---|---|
| `core/fixtures/api_fixtures.py` | Imports `api_tests.services.{devices_service,health_service,test_admin_service}`; `/api/login`, token field and reference service fixtures | Move auth/service fixtures to consumer-owned fixture module; keep generic request context and API client |
| `core/fixtures/data_fixtures.py` | Imports device factory and creates/deletes reference devices | Move device lifecycle fixtures to consumer-owned test support |
| `core/test_data/{device_factory,invalid_device_factory}.py` | Reference device payloads | Move factories to consumer-owned test data; inspect invalid factory implementation before moving |
| `core/schemas/device_schemas.py` | Device-specific JSON Schema | Move schema to consumer test support; preserve generic schema assertions |
| `core/fixtures/ui_fixtures.py` | Imports `ui_tests.pages.login_page.LoginPage` | Move `login_page` fixture to consumer; keep generic trace `output_path` |
| Root `conftest.py` | Session autouse `reset_backend_after_test_session` invokes `test_admin_service.reset_test_data()` | Move reference reset orchestration to consumer configuration; preserve protected-environment and xdist behavior |
| `core/config/environments.yaml` | FastAPI hostnames, admin usernames and FormCircles staging URL | Separate framework config loader from reference environment values; preserve CLI > env > YAML behavior |
| `core/config/settings.py` | `approved_ci_target = "http://127.0.0.1:8080"` | Replace with explicit configurable CI target allowlist, **fail closed**; never remove safety check without equivalent tests |

## Intentional reference validation

`api_tests/`, `ui_tests/`, the reference SUT, and the three GitHub Actions workflows can depend on the framework and launch/test FastAPI. These are consumers and integration verification, not prohibited core imports. Workflow-specific FastAPI image names, `/health`, and `TEST_PASSWORD` should be documented as reference-SUT integration configuration rather than framework-only defaults.

## Generic core to retain

Generic `APIClient`, Playwright request context, base URL validation, configuration precedence, JSON Schema assertions, API logging, screenshot/trace artifact handling, and reusable cleanup/environment guard mechanisms. Generic mechanisms must remain independent of device schemas and application login/reset endpoints.

## Targeted review and verification gaps

- Review `core/cleanup/backend_reset.py`, `core/environment/environment_guard.py`, and `core/fixtures/base_fixtures.py` for application-specific assumptions and credential naming.
- Review complete `core/test_data/invalid_device_factory.py` and `core/schemas/device_schemas.py` implementations when moving them.
- Review root `pytest_plugins` registration after fixture relocation so consumer-only fixtures are not exposed as public PETF fixtures.
- Inventory was static: dynamic imports, runtime injection, Docker entrypoints and all complete workflow contents were **not exhaustively inspected**.
- `Needs targeted review` rows remain explicit follow-up work; do not treat these as verified clean.

## Proposed PETF-90 implementation sequence (reconcile with existing Jira subtasks)

1. Consumer-owned API auth/service fixtures; preserve API regression coverage.
2. Consumer-owned device factories, schemas, create/delete cleanup fixtures.
3. Consumer-owned UI page fixture; preserve Playwright page lifecycle and trace behavior.
4. Config separation and configurable CI target allowlist with fail-closed tests.
5. Consumer-owned session reset, retaining serial/xdist/protected-environment guarantees.
6. CI dependency-direction check prohibiting `core` imports from `api_tests`, `ui_tests`, or `sut`.

## Acceptance / completion notes

PETF-91 delivers an inventory and architecture classification, **not a production refactor**. Before merging, verify the CSV row count, review outstanding targeted-review items, run existing quality checks as appropriate, and confirm the documentation is consistent with the actual repository. PETF-90 implementation work should use small, independently testable changes. Do not change existing CI safety or reset behavior as part of this documentation-only subtask.
