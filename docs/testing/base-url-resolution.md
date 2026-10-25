# BASE_URL Resolution and Execution Environments

## Overview

PETF resolves the application URL using consistent configuration
precedence across supported execution environments.

Configuration files:

- `core/config/settings.py`: Configuration resolver and validation.
- `core/config/environments.yaml`: Environment-specific defaults.
- `core/config/pytest_options.py`: Explicit pytest option detection.

## Configuration Precedence

The application BASE_URL is resolved in this order:

1. Explicit pytest `--base-url` option.
2. `BASE_URL` environment variable.
3. `PYTEST_BASE_URL` environment variable.
4. Selected environment's YAML configuration.

The highest-priority available value wins.

Invalid higher-priority values are rejected rather than replaced
with lower-priority configuration values.

The default supplied by the pytest-base-url plugin does not
count as an explicit command-line override.

## Supported Environments

| Environment | Default BASE_URL |
|-------------|------------------|
| local | http://127.0.0.1:8080 |
| dev | http://127.0.0.1:8080 |
| ci | http://127.0.0.1:8080 |
| docker | http://fastapi:8080 |
| k8s | http://fastapi-mock-app:8080 |
| staging | https://staging.api.formcircles.com |

## Local Execution

Run tests against the locally running FastAPI application:

```bash
pytest --env=local
```

Override the URL explicitly:

```bash
pytest --env=local --base-url=http://127.0.0.1:9090
```

Alternatively, use an environment variable:

```bash
export BASE_URL=http://127.0.0.1:9090
pytest --env=local
```

An explicit `--base-url` takes precedence over `BASE_URL`.

## Docker Execution

The Docker test runner selects the `docker` environment by default.

The configured application URL is `http://fastapi:8080`,
which uses the FastAPI service hostname on the Compose network.

The runner supports environment selection through `PETF_ENV`.

Example:

```bash
PETF_ENV=docker ./scripts/run-tests.sh
```

The `BASE_URL` environment variable can override the Docker
environment's configured URL.

## CI Execution and Safety

GitHub Actions workflows explicitly select the `ci` environment.

Example:

```bash
pytest -m smoke --env=ci
```

The only approved CI application URL is:

`http://127.0.0.1:8080`

When the `ci` environment is selected, PETF rejects any
other resolved BASE_URL.

This restriction applies to URLs supplied through:

- Explicit pytest `--base-url` options.
- The `BASE_URL` environment variable.
- The `PYTEST_BASE_URL` environment variable.
- Environment YAML configuration.

PETF validates the CI target during pytest session startup,
before test collection begins.

An unsafe target causes pytest to terminate with an error.

This prevents accidental CI execution against an unintended
application endpoint.

The restriction does not apply to other environments.

## URL Validation

BASE_URL must be a non-empty HTTP or HTTPS URL.

PETF rejects malformed URLs and URLs containing credentials,
query parameters, fragments, or whitespace.

Invalid ports are also rejected.

## Troubleshooting

### Tests target an unexpected application

Check the configuration sources in precedence order:

1. Explicit `--base-url` option.
2. `BASE_URL` environment variable.
3. `PYTEST_BASE_URL` environment variable.
4. Selected environment in `core/config/environments.yaml`.

### CI rejects BASE_URL

The `ci` environment permits only:

`http://127.0.0.1:8080`

Use the appropriate environment for other approved test targets.

### Docker cannot resolve the application hostname

Confirm that the FastAPI service is running on the expected
Docker Compose network.

Verify that the selected environment is `docker`.

### Unknown environment error

Check that the requested environment exists in
`core/config/environments.yaml`.

## PETF v1.1 Fixture and Operational Notes

The session-scoped `settings` fixture resolves configuration in
`core/config/settings.py`. For `base_url`, precedence is explicit pytest
`--base-url` (including `PYTEST_ADDOPTS`), `BASE_URL`, `PYTEST_BASE_URL`,
then selected environment YAML. A plugin-provided default is not an explicit
override. Invalid higher-priority values fail rather than falling back.

Pytest defaults to `--env=local`; supported choices are `local`, `dev`,
`ci`, `docker`, `k8s`, and `staging`. The Docker runner can select its
environment using `PETF_ENV`. In `ci`, PETF validates the resolved URL at
session startup and permits only `http://127.0.0.1:8080`.

The `base_url`, `test_username`, and `test_password` fixtures expose
resolved settings. `TEST_USERNAME` can override the environment's username;
`TEST_PASSWORD` is read from the process environment and may be empty until
an authenticated test requires it. The session-scoped `api_request_context`
uses the configured base URL and request timeout, and is disposed during
teardown. `public_api_client` reuses it without an auth token. The UI
`output_path` fixture reserves a distinct worker-safe Playwright directory
for each test. See the artifact contract for current output locations.
