# PETF-101 — Execution Mode Compatibility Verification

## 1. Overview

| Field | Value |
|---|---|
| Jira issue | PETF-101 |
| Parent | PETF-99 |
| Project | Playwright Enterprise Test Framework (PETF) |
| Release | v1.1 |
| Sprint | 2026-Q4-S1 |
| Verification date | 2026-10-24 |
| Outcome | **PASS with documented limitations** |

**Objective:** Verify PETF across local serial, experimental parallel API, Docker, and local CI-mode execution. An actual GitHub Actions run was not performed.

## 2. Verification Environment

| Component | Host | Docker test runner |
|---|---|---|
| OS/base | Ubuntu 22.04 | Python 3.12 slim |
| Python | 3.10.12 | 3.12.15 |
| pytest | 9.1.1 | 9.1.1 |
| pytest-xdist | 3.8.0 | 3.8.0 |
| Reference SUT | FastAPI on `127.0.0.1:8080` | FastAPI on `fastapi:8080` |

Docker Engine: 29.1.3. The Docker runner included Playwright browsers and system dependencies.

## 3. Execution Mode Verification Matrix

| Mode | Scope | Result | Assessment |
|---|---|---|---|
| Local serial | API regression | 9 passed | PASS |
| Experimental parallel | API regression, 2 workers, `loadscope` | 9 passed | PASS (experimental scope only) |
| Docker | API + UI smoke | 2 passed | PASS |
| Docker | Complete API test directory | 305 passed, 1 skipped | PASS |
| Local CI mode | API + UI smoke | 2 passed | PASS |
| GitHub Actions | Actual hosted workflow | Not executed | NOT VERIFIED |

No test failures were observed in the executed verification suites.

## 4. Local Serial Execution

```bash
TEST_USERNAME=admin TEST_PASSWORD=password BASE_URL=http://127.0.0.1:8080 \
  python -m pytest -q -m "api and regression" --env=local \
  --junitxml=/tmp/petf-101-local-serial-junit.xml
```

**Result:** 9 passed in approximately 0.94 seconds. Local serial remains the default execution mode.

## 5. Experimental Parallel API Execution

```bash
TEST_USERNAME=admin TEST_PASSWORD=password BASE_URL=http://127.0.0.1:8080 \
  python -m pytest -q -m "api and regression" --env=local \
  -n 2 --dist loadscope \
  --junitxml=/tmp/petf-101-parallel-api-junit.xml
```

**Result:** 9 passed in approximately 1.51 seconds. This small selection ran more slowly than serial execution. The passing result applies only to the approved two-worker API regression experiment; it does **not** approve parallel UI tests, `-n auto`, larger worker counts, or the full suite in parallel.

## 6. Docker Execution

### Images and network

- SUT image: `petf-101-fastapi-sut:local` (approximately 161 MB).
- Test-runner image: `petf-101-test-runner:local` (approximately 2.5 GB).
- Isolated network: `petf-101-network`, with SUT alias `fastapi`.
- Container-to-container health request: `GET http://fastapi:8080/health` returned HTTP 200 and `{"status":"ok"}`.
- SUT was not bound to host port 8080; the existing host SUT was unaffected.

### Docker smoke tests

Runner environment: `PETF_ENV=docker`, `TEST_SUITE=smoke`, credentials supplied through test environment variables.

**Result:** 2 passed, 311 deselected in 1.44 seconds. The API health and Chromium UI login smoke tests passed.

Reports: `smoke-junit-results.xml`, `smoke-report.html`.

### Docker API tests

Runner environment: `PETF_ENV=docker`, `TEST_SUITE=api`.

**Result:** 305 passed, 1 skipped, 0 failed in 11.37 seconds. The skipped case was an opt-in interrupt probe (`PETF88_INTERRUPT=1`) that was intentionally not enabled.

Reports: `api-junit-results.xml`, `api-report.html`.

**Assessment:** PASS for the executed Docker smoke and API suites, not for every possible Docker deployment configuration.

## 7. CI-Mode Verification

```bash
TEST_USERNAME=admin TEST_PASSWORD=password BASE_URL=http://127.0.0.1:8080 \
  python -m pytest -v -m smoke --env=ci \
  --junitxml=/tmp/petf-101-ci-smoke-junit.xml \
  --html=/tmp/petf-101-ci-smoke-report.html --self-contained-html
```

**Result:** 2 passed, 311 deselected in 1.34 seconds. API health and Chromium UI login smoke tests passed. Both JUnit XML and HTML reports were generated.

**Local CI-mode assessment:** PASS. This local simulation used
Python 3.10.12, while the GitHub Actions workflow targets Python 3.12.

### GitHub-Hosted Workflow Verification

Following the initial local verification, PR #100 was opened,
successfully checked, and merged into `main`.

Observed successful GitHub Actions workflows:

| Workflow | Context | Result |
|---|---|---|
| Run Tests | PR #100 | PASS |
| Build Test Publish Container | PR #100 | PASS |
| Run Published Container | PR #100 | PASS |
| Run Tests | Merged `main` | PASS |
| Build Test Publish Container | Merged `main` | PASS |

Merge commit: `df89588`.

The GitHub Actions workflow results provide hosted CI evidence
beyond the original local CI-mode simulation.

**Assessment:** PASS for the observed GitHub-hosted workflows.
The verification does not establish compatibility with every
possible CI configuration.

## 8. Configuration Compatibility

| PETF environment | YAML base URL |
|---|---|
| `local` | `http://127.0.0.1:8080` |
| `docker` | `http://fastapi:8080` |
| `ci` | `http://127.0.0.1:8080` |

`core/config/settings.py` resolves URL configuration with precedence **CLI override > environment variable > environment YAML**. Shared fixtures reference `settings.base_url`. The Docker test-runner independently reached `http://fastapi:8080/health` successfully.

**Observation:** `pytest.ini` also defines `base_url = http://127.0.0.1:8080`; pytest-playwright displayed that value during Docker runs. The walkthrough did not trace every individual test request, so it does not prove all integration tests used the Docker-specific PETF URL. Review these two configuration paths separately.

## 9. Operational Safety

The dedicated `petf-101-sut` container and `petf-101-network` were removed after testing. The two PETF-101 images were retained. Existing containers `nice_murdock`, `squid_proxy_1`, and `portainer` remained running. No tracked repository files were changed during execution checks; the unrelated untracked `artifacts/` directory was left untouched.

## 10. Limitations and Follow-Up Recommendations

1. **Actual GitHub Actions execution — VERIFIED.** PR #100 and post-merge workflows completed successfully.
2. **Base URL consistency — OBSERVATION.** Confirm pytest-playwright and PETF Settings consistently select the intended target for each environment.
3. **Docker image size — OPTIMIZATION OPPORTUNITY.** The ~2.5 GB runner image may warrant future optimization; it did not block verification.
4. **Parallel execution — EXPERIMENTAL.** Retain serial as the default; require separate approval and testing before expanding worker counts or UI parallelism.
5. **Docker build reliability — OBSERVATION.** Browser downloads experienced transient timeouts but recovered and the image built successfully.

## 11. Final Assessment

**PASS WITH DOCUMENTED LIMITATIONS** for the selected local serial, experimental two-worker API, Docker smoke/API, and local CI-mode suites. No executed tests failed. Subsequent GitHub Actions runs passed for PR #100 and the merged main branch. This result does not authorize unrestricted parallel execution.

**Recommended Jira disposition:** PETF-101 may be completed after review and commit of this record **if** its acceptance criteria do not require an actual hosted CI run. Track unverified requirements separately.

## 12. Evidence Summary

| Evidence | Observed result |
|---|---|
| Local serial JUnit | 9 passed |
| Experimental parallel JUnit | 9 passed |
| Docker smoke JUnit | 2 passed |
| Docker API JUnit | 305 passed, 1 skipped |
| Local CI smoke JUnit | 2 passed |
| GitHub Actions PR #100 | 3 workflows passed |
| GitHub Actions merged main | 2 workflows passed |
| Docker health request | HTTP 200 |
| Docker cleanup | Successful |
| Unrelated containers | Unaffected |

Reports were generated in temporary host directories during the walkthrough and are not embedded in this document. This record summarizes the observed terminal results rather than independently rerunning the tests.

## 13. Conclusion

PETF-101 demonstrated successful execution of the selected test suites in the tested modes. Subsequent GitHub Actions workflows also passed. Exhaustive cross-environment request tracing and broader parallel configurations remain unverified.

**Final recommendation: PASS WITH DOCUMENTED LIMITATIONS.**
