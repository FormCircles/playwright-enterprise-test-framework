# PETF v1.1 Consumer Compatibility and Migration Guide

Status: Q4-S1 implementation checkpoint; v1.1.0 not yet released.
Baseline: PETF v1.0.0.
Tracking: PETF-103 / PETF-105.

## Compatibility Summary

PETF v1.1 includes consumer-facing behavioral changes.
Existing product test suites should review the migration requirements
before adopting the checkpoint.

## Configuration Changes

BASE_URL resolution now follows this precedence:

1. Explicit pytest --base-url option.
2. BASE_URL environment variable.
3. PYTEST_BASE_URL environment variable.
4. Selected environment YAML configuration.

Invalid higher-priority values fail validation rather than falling back.

The ci environment permits only http://127.0.0.1:8080.
Consumers targeting another host must use an appropriate environment
configuration instead of bypassing the CI safety restriction.

The docker environment default changed from app:8080 to fastapi:8080.
Verify service discovery and override BASE_URL where necessary.

TEST_USERNAME remains configurable through the environment.
TEST_PASSWORD remains an environment variable.

## Fixture Migration

Shared core fixtures continue to include settings, base_url,
test_username, test_password, api_request_context, and public_api_client.

Application-specific fixtures were removed from shared core,
including auth_token, auth_header, api_client, devices_service,
health_service, test_admin_service, and device-data fixtures.

Consumers depending on those fixtures must provide their own
application-specific implementations.

The login_page fixture is now registered by the reference UI suite.
Product test suites should register their own page-object fixtures.

The session-scoped API request context is explicitly disposed
during fixture teardown. Do not retain it beyond the session.

Automatic backend reset at session completion was removed.
Consumers requiring backend cleanup must implement their own
safe cleanup policy.

## Tracing and Diagnostics

PETF adds --petf-trace=off and --petf-trace=on-failure.

Do not combine --petf-trace with an explicit native --tracing option.

Failure screenshots are captured for eligible failed UI test calls.
Screenshots may contain sensitive application data and are not
automatically redacted.

## Artifact Migration

Existing producers continue writing to test-results/.

CI collection stages available artifacts under artifacts/<run-id>/,
including reports/, metadata/, and legacy/ when applicable.

Consumers parsing downloaded CI artifacts must account for the
new staging structure.

Canonical producer paths remain a future migration target.
Do not assume all producers already use the canonical layout.

Artifact publication is subject to security verification.
Failed verification blocks publication.

## Consumer Migration Checklist

- Review BASE_URL precedence and URL validation.
- Verify the selected execution environment.
- Update Docker service hostname assumptions.
- Replace removed application-specific fixtures.
- Register product-specific page-object fixtures.
- Review API context lifetime assumptions.
- Implement application-specific cleanup where required.
- Review trace command-line options.
- Update CI artifact discovery paths where necessary.
- Review artifact access and retention for sensitive information.
- Run consumer regression tests before adoption.

## Breaking Change Assessment

Known compatibility impacts are documented above.

Zero undocumented breaking changes is an acceptance objective,
not yet a verified conclusion.

Final confirmation requires consumer-facing regression evidence,
review of supported extension contracts, and resolution of any
additional compatibility findings.

## Related Documentation

- [BASE_URL resolution](../testing/base-url-resolution.md)
- [Artifact directory contract](../architecture/artifact-directory-contract.md)
- [CI artifact publication](../operations/ci-artifact-publication.md)
- [Screenshot hygiene](../screenshot-artifact-hygiene.md)
- [Trace activation](../trace-activation-policy.md)
