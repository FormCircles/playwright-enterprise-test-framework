# Playwright Enterprise Test Framework

Enterprise-grade Playwright automation framework demonstrating scalable UI and API testing, Page Object Model (POM) architecture, CI/CD, Docker, and a realistic FastAPI-based System Under Test (SUT).

The project is designed as a real-world enterprise automation framework rather than a collection of sample tests. It demonstrates how modern QA and SDET teams organize browser automation for maintainability, scalability, and continuous integration.

---

## Project Goals

The Playwright Enterprise Test Framework was built to demonstrate enterprise automation engineering practices including:

* Maintainable Page Object Model architecture
* Browser automation using Microsoft Playwright
* API testing with pytest
* Enterprise project organization
* CI/CD with GitHub Actions
* Docker-based execution
* Parallel test execution
* HTML and JUnit reporting
* Environment-based configuration
* Accessibility-aware UI automation
* Realistic FastAPI Mock Application (SUT)

The framework is intended to serve both as a professional portfolio project and as the foundation for future enterprise automation initiatives.

## Contents

- Features
- Architecture
- Repository Structure
- Quick Start
- Installation
- Configuration
- Running Tests
- FastAPI Mock Application
- Docker and Docker Compose
- Continuous Integration
- Roadmap
- Contributing
- License


---

## Features

## UI Automation

* Microsoft Playwright
* Chromium browser automation
* Page Object Model (POM)
* Stable `data-testid` selectors
* Accessibility-aware locators
* Login automation
* Device Management CRUD automation
* Reusable page objects

## API Automation

* pytest-based API testing
* Authentication testing
* CRUD validation
* Structured test organization

## Framework Features

* pytest
* pytest-xdist parallel execution
* Environment configuration
* Base URL configuration
* Structured logging
* Failure diagnostics
* HTML reports
* JUnit XML reports
* Configurable test markers

## Infrastructure

* Docker support
* Docker Compose
* GitHub Actions
* GitHub Container Registry (GHCR)
* Health checks
* Automated smoke testing

---

## Architecture

The framework separates browser automation from application logic through reusable page objects.

```text
                    +----------------------+
                    |   Playwright Tests   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |     Page Objects     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |  FastAPI Mock App    |
                    |   (System Under      |
                    |      Test - SUT)     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Device Data Store    |
                    +----------------------+
```

The FastAPI Mock Application provides a realistic enterprise web application used by the Playwright framework for browser automation. It includes authentication, device management, accessibility improvements, stable automation selectors, and realistic CRUD workflows.

The SUT is maintained as a Git submodule to keep the automation framework and application under test cleanly separated.

---

## Repository Structure

```text
playwright-enterprise-test-framework/
│
├── api_tests/                 # API automation tests
├── core/                      # Shared framework components
│   ├── config/
│   ├── fixtures/
│   ├── logging/
│   ├── services/
│   ├── test_data/
│   └── utils/
│
├── docs/                      # Project documentation
│
├── ui_tests/
│   ├── pages/                 # Page Object Model
│   └── tests/                 # Playwright browser tests
│
├── sut/
│   └── FastAPIMockApp/        # FastAPI Mock Application (Git submodule)
│
├── test-results/              # Generated reports
├── .github/                   # GitHub Actions workflows
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Technology Stack

| Category           | Technology                |
| ------------------ | ------------------------- |
| Language           | Python 3.12+              |
| UI Automation      | Playwright                |
| Test Framework     | pytest                    |
| API Testing        | pytest                    |
| Parallel Execution | pytest-xdist              |
| Reporting          | pytest-html, JUnit XML    |
| Web Framework      | FastAPI                   |
| CI/CD              | GitHub Actions            |
| Containers         | Docker                    |
| Registry           | GitHub Container Registry |
| Version Control    | Git + GitHub              |

---

## Quick Start


# Quick Start

## Prerequisites

Install:

- Python 3.12+
- Git
- Docker (optional)
- Google Chrome or Chromium

---

## Clone the Repository

```bash
git clone https://github.com/FormCircles/playwright-enterprise-test-framework.git

cd playwright-enterprise-test-framework
```

---

## Initialize the FastAPI Mock Application

```bash
git submodule update --init --recursive
```

---

## Create a Virtual Environment

Linux/macOS:

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

---

## Install Dependencies

```bash
python -m pip install --upgrade pip

python -m pip install -r requirements.txt
```

Install the Playwright browser:

```bash
python -m playwright install chromium
```

---

## Start the FastAPI Mock Application

Open a new terminal:

```bash
cd sut/FastAPIMockApp

uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8080
```

The application should now be available at:

```
http://127.0.0.1:8080
```

---

## Configure Test Credentials

Return to the project root:

```bash
export TEST_USERNAME=<test-username>
export TEST_PASSWORD=<test-password>
```

Use the credentials configured for your local FastAPI Mock Application.

---

## Run a Smoke Test

```bash
python -m pytest \
    -m smoke \
    --env=dev \
    --base-url=http://127.0.0.1:8080 \
    -v
```

---

## Expected Result

You should see:

- Playwright launches Chromium
- Login succeeds
- Smoke tests pass
- HTML and JUnit reports are generated

Congratulations! The Playwright Enterprise Test Framework is now running successfully.


## Installation

## Prerequisites

Before using the framework, ensure the following software is installed:

| Software                    | Recommended Version                |
| --------------------------- | ---------------------------------- |
| Python                      | 3.12 or later                      |
| Git                         | Latest                             |
| Playwright                  | Latest Python package              |
| Chromium                    | Installed via `playwright install` |
| Docker *(optional)*         | Latest                             |
| Docker Compose *(optional)* | Latest                             |

---

## Clone the Repository

```bash
git clone https://github.com/FormCircles/playwright-enterprise-test-framework.git

cd playwright-enterprise-test-framework
```

---

## Initialize the FastAPI Mock Application

The FastAPI Mock Application (SUT) is maintained as a Git submodule.

Initialize it after cloning:

```bash
git submodule update --init --recursive
```

Verify:

```bash
git submodule status
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

Linux/macOS

```bash
source .venv/bin/activate
```

Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

---

## Install Python Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## Install Playwright Browsers

```bash
playwright install
```

To install only Chromium:

```bash
playwright install chromium
```

---

## Configuration

For BASE_URL precedence, execution environments, and CI safety,
see [BASE_URL Resolution and Execution Environments](docs/testing/base-url-resolution.md).

The framework supports environment-based execution.

Configuration values may be supplied using environment variables or your preferred configuration mechanism.

## Base URL

Example:

```text
http://127.0.0.1:8080
```

Example:

```bash
export BASE_URL=http://127.0.0.1:8080
```

---

## Test Credentials

Example:

```bash
export TEST_USERNAME=<test-username>
export TEST_PASSWORD=<test-password>
```

These credentials are used by authenticated browser tests.

> Note: Replace these placeholders with credentials configured for your local FastAPI Mock Application.

---

## Environment Selection

Examples:

```bash
pytest --env=dev

pytest --env=local

pytest --env=staging
```

Each environment can provide its own:

* Base URL
* Credentials
* Environment-specific configuration

---

## Running the FastAPI Mock Application

Start the FastAPI Mock Application from the SUT directory.

```bash
cd sut/FastAPIMockApp
```

Activate the virtual environment if needed.

```bash
source ../../.venv/bin/activate
```

Start the application.

```bash
python -m uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8080
```

The application will be available at:

```text
http://127.0.0.1:8080
```

---

## Running Tests

All tests

```bash
pytest
```

Verbose output

```bash
pytest -v
```

Collect tests only

```bash
pytest --collect-only
```

---

## Smoke Tests

```bash
pytest -m smoke
```

---

## Regression Tests

```bash
pytest -m regression
```

---

## UI Tests

```bash
pytest -m ui
```

---

## API Tests

```bash
pytest -m api
```

---

## Authentication Tests

```bash
pytest -m auth
```

---

## Slow Tests

```bash
pytest -m slow
```

---

## Combined Marker Examples

Smoke UI tests

```bash
pytest -m "smoke and ui"
```

Regression UI tests

```bash
pytest -m "regression and ui"
```

Exclude slow tests

```bash
pytest -m "not slow"
```

Run smoke tests against a specific environment

```bash
pytest \
    -m smoke \
    --env=dev \
    --base-url=http://127.0.0.1:8080
```

---

## Parallel Execution

The framework supports parallel execution using **pytest-xdist**.

Recommended:

```bash
pytest \
    -n 2 \
    --dist loadscope
```

This configuration keeps related tests together while improving execution time.

Current recommendation:

* ✅ `-n 2`
* ✅ `--dist loadscope`

Avoid:

```bash
pytest -n auto
```

for tests that share mutable backend state, as this can introduce race conditions.

---

## Test Markers

The framework organizes tests using pytest markers.

| Marker     | Purpose               |
| ---------- | --------------------- |
| smoke      | Critical smoke tests  |
| regression | Full regression suite |
| ui         | Browser automation    |
| api        | API automation        |
| auth       | Authentication tests  |
| slow       | Long-running tests    |

Examples:

Run smoke UI tests

```bash
pytest -m "smoke and ui"
```

Run API regression tests

```bash
pytest -m "api and regression"
```

Exclude slow tests

```bash
pytest -m "not slow"
```

---

## Test Reports

The framework supports multiple reporting formats.

## HTML Report

```bash
pytest \
    --html=test-results/report.html \
    --self-contained-html
```

---

## JUnit XML

```bash
pytest \
    --junitxml=test-results/junit-results.xml
```

---

## Generate Both Reports

```bash
pytest \
    --html=test-results/report.html \
    --self-contained-html \
    --junitxml=test-results/junit-results.xml
```

Generated output:

```text
test-results/
├── report.html
└── junit-results.xml
```

These reports are automatically generated during GitHub Actions CI runs and can also be produced locally.

---

## Failure Diagnostics

The framework captures useful diagnostic information when tests fail.

Current capabilities include:

* Structured logging
* HTML reports
* JUnit XML
* Browser screenshots *(where applicable)*
* Playwright trace support *(future enhancement)*

The goal is to simplify debugging while providing actionable failure information during both local development and CI execution.


## FastAPI Mock Application (System Under Test)

## Overview

The Playwright Enterprise Test Framework includes a realistic FastAPI-based System Under Test (SUT).

Rather than relying on public demo websites, the framework uses its own web application to provide stable, repeatable, and deterministic browser automation.

The FastAPI Mock Application is maintained as a Git submodule, allowing the automation framework and application under test to evolve independently while remaining tightly integrated.

Repository location:

```text
sut/
└── FastAPIMockApp/
```

---

## Purpose

The SUT provides a realistic enterprise web application for validating:

* User authentication
* Browser automation
* Device management workflows
* CRUD operations
* API testing
* Accessibility
* Stable automation selectors

This approach allows the Playwright framework to simulate enterprise QA workflows without depending on external services.

---

## Current Features

### Authentication

* Login page
* Username/password authentication
* Authentication validation
* Invalid login handling

### Device Management

* View device list
* Create devices
* Edit devices
* Delete devices

### API Endpoints

* Login
* Device CRUD operations
* Validation
* Error handling

### Accessibility

The UI includes accessibility improvements designed for both end users and automated testing.

Examples include:

* Proper `<label>` elements
* Accessible form controls
* ARIA roles
* Status messages
* Alert messages

---

## Stable Automation Selectors

The application exposes dedicated automation selectors using `data-testid`.

Examples include:

```text
create-device-name
create-device-status
create-device-submit

device-row-1

edit-device-1
delete-device-1

edit-device-name
edit-device-status
edit-device-save

operation-success
```

These selectors provide stable browser automation that is resistant to UI layout changes.

---

## Playwright Page Object Model

The framework follows the Page Object Model (POM) design pattern.

Current page objects include:

```text
ui_tests/
└── pages/
    ├── base_page.py
    ├── login_page.py
    └── devices_page.py
```

Responsibilities:

## BasePage

Provides reusable browser operations:

* Navigation
* Clicking
* Filling inputs
* Waiting
* Assertions

---

## LoginPage

Encapsulates authentication workflows.

Examples:

* Open login page
* Enter credentials
* Submit login
* Verify login

---

## DevicesPage

Encapsulates device management operations.

Examples:

* Open device page
* Create device
* Edit device
* Delete device
* Verify success messages
* Verify device visibility
* Verify device removal

Browser tests interact only with page objects rather than directly with Playwright locators.

---

## Docker Support

The framework supports execution inside Docker containers.

Typical workflow:

```text
Developer
      │
      ▼
Docker Build
      │
      ▼
Playwright Container
      │
      ▼
Execute Tests
      │
      ▼
Generate Reports
```

Benefits include:

* Consistent execution environment
* Simplified dependency management
* Repeatable CI execution
* Easy onboarding for new developers

Build the image:

```bash
docker build -t playwright-enterprise-test-framework .
```

Run the container:

```bash
docker run --rm playwright-enterprise-test-framework
```

---

## Docker Compose

Docker Compose simplifies local development by orchestrating multiple services.

Example:

```bash
docker compose up
```

Typical services include:

* Playwright test runner
* FastAPI Mock Application

Docker Compose provides a reproducible local environment similar to CI.

---

## Continuous Integration

The project uses GitHub Actions to automate testing.

High-level workflow:

```text
GitHub Push / Pull Request
              │
              ▼
Checkout Repository
              │
              ▼
Initialize Submodule
              │
              ▼
Create Python Environment
              │
              ▼
Install Dependencies
              │
              ▼
Install Playwright Browsers
              │
              ▼
Start FastAPI Mock App
              │
              ▼
Execute Tests
              │
              ▼
Generate Reports
              │
              ▼
Publish Artifacts
```

The pipeline automatically validates browser automation before code is merged.

---

## GitHub Container Registry (GHCR)

The FastAPI Mock Application is published as a container image using GitHub Container Registry.

Typical workflow:

```text
Build Container
       │
       ▼
Push to GHCR
       │
       ▼
Pull Latest Image
       │
       ▼
Run Smoke Tests
```

Using GHCR provides:

* Versioned container images
* Repeatable deployments
* Consistent CI execution
* Simple image distribution

---

## Smoke Testing

The CI pipeline executes smoke tests against the deployed FastAPI Mock Application.

Smoke testing validates that:

* Application starts successfully
* Login works
* Browser automation functions correctly
* Core workflows remain operational

Smoke tests provide rapid feedback while minimizing execution time.

---

## Reports and Artifacts

GitHub Actions automatically publishes test artifacts.

Generated artifacts include:

```text
test-results/
├── report.html
├── junit-results.xml
└── screenshots/          (future enhancement)
```

These artifacts assist with debugging CI failures and reviewing execution results.

---

## Enterprise Development Workflow

Development follows a feature-branch workflow.

```text
Feature Branch
      │
      ▼
Development
      │
      ▼
Local Validation
      │
      ▼
Pull Request
      │
      ▼
GitHub Actions
      │
      ▼
Code Review
      │
      ▼
Merge to Main
```

Each feature is tracked through Jira and implemented using small, reviewable pull requests.

---

## Current Framework Capabilities (v1.0)

## Browser Automation

* Login workflow
* Device CRUD workflow
* Page Object Model
* Accessibility-aware locators
* Stable automation selectors

## API Testing

* Authentication
* Device CRUD
* Validation
* Error handling

## Framework

* pytest
* Playwright
* Page Object Model
* Environment configuration
* Test markers
* Structured logging
* Failure diagnostics
* Parallel execution

## Infrastructure

* Docker
* Docker Compose
* GitHub Actions
* GitHub Container Registry
* FastAPI Mock Application
* HTML reports
* JUnit XML reports

The v1.0 release establishes a solid enterprise automation foundation that can be extended with additional browser coverage, API scenarios, visual testing, Kubernetes-based execution, and distributed test execution in future releases.


## Roadmap

The Playwright Enterprise Test Framework follows an incremental roadmap focused on building a production-quality enterprise automation platform.

---

## Version 1.0 (Target Release)

The v1.0 release establishes the core automation framework.

### Framework

* Enterprise project structure
* Page Object Model (POM)
* Environment configuration
* Test marker taxonomy
* Structured logging
* Failure diagnostics
* HTML reporting
* JUnit XML reporting
* Parallel execution with pytest-xdist

### UI Automation

* Login workflow
* Device Management UI
* Create Device
* Edit Device
* Delete Device
* Accessibility-aware automation
* Stable `data-testid` selectors

### API Automation

* Authentication
* Device CRUD
* Validation testing

### Infrastructure

* FastAPI Mock Application
* Docker support
* Docker Compose
* GitHub Actions
* GitHub Container Registry (GHCR)
* Automated smoke testing

---

## Planned Enhancements

Future releases will continue expanding the framework while maintaining a clean, enterprise architecture.

### Cross-Browser Testing

* Microsoft Edge
* Firefox
* WebKit
* Browser compatibility matrix

---

### Expanded Test Coverage

* Advanced authentication scenarios
* Role-based authorization
* Negative testing
* File upload/download
* Session management
* Error handling
* Large dataset validation

---

### Visual Testing

Potential future capabilities include:

* Screenshot comparison
* Visual regression detection
* Responsive layout validation

---

### Accessibility Automation

Expand accessibility validation with:

* Automated accessibility scanning
* WCAG validation
* Keyboard navigation testing
* Screen reader compatibility

---

### Performance Validation

Future browser performance testing may include:

* Page load timing
* Network performance
* Browser rendering metrics

---

### Container-Native Execution

Expand Docker support with:

* Multi-stage builds
* Optimized Playwright containers
* Containerized execution environments

---

### Kubernetes

Following the v1.0 release, Kubernetes becomes the next major infrastructure milestone.

Planned capabilities include:

* Containerized FastAPI Mock Application
* Kubernetes deployment manifests
* Helm charts
* Playwright execution against Kubernetes services
* CI integration
* Scalable execution
* Foundation for distributed browser testing

---

### Cloud Execution

Potential future support includes:

* GitHub-hosted runners
* Self-hosted runners
* Cloud-based browser execution
* Distributed automation

---

## Version History

| Version | Status  | Highlights                           |
| ------- | ------- | ------------------------------------ |
| v1.0    | In preparation | Initial enterprise release           |
| v1.1    | Planned | Expanded browser automation          |
| v1.2    | Planned | Kubernetes integration               |
| v2.0    | Future  | Enterprise-scale automation platform |

---

## Contributing

Contributions are welcome.

Recommended development workflow:

1. Create a feature branch.
2. Implement the requested change.
3. Execute local validation.
4. Ensure all automated tests pass.
5. Submit a Pull Request.
6. Complete code review before merging.

Example:

```bash
git checkout -b feature/my-new-feature
```

Commit your work:

```bash
git commit -m "Implement new feature"
```

Push the branch:

```bash
git push origin feature/my-new-feature
```

Open a Pull Request for review.

---

## Development Philosophy

The project follows several core engineering principles.

## Build for Maintainability

Favor readability, modularity, and long-term maintainability over short-term convenience.

---

## Enterprise Architecture

Organize code using patterns commonly found in production automation frameworks.

Examples include:

* Page Object Model
* Shared fixtures
* Reusable services
* Environment abstraction
* Clear separation of concerns

---

## Automation First

Automate repetitive engineering tasks whenever practical.

Examples include:

* Test execution
* Reporting
* Continuous Integration
* Container builds

---

## Continuous Improvement

The framework is intentionally designed to evolve incrementally.

Each release builds upon a stable foundation while introducing new capabilities without sacrificing maintainability.

---

## License

This project is licensed under the MIT License.

See the LICENSE file for additional details.

---

## Acknowledgements

This project is built using several outstanding open-source technologies.

* Microsoft Playwright
* pytest
* FastAPI
* Docker
* GitHub Actions
* Python

Special thanks to the open-source community for providing the tools that make modern automation engineering possible.

---

## Contact

**Author**

Joseph Doan

GitHub: https://github.com/FormCircles

---

## Final Notes

The Playwright Enterprise Test Framework demonstrates how modern enterprise browser automation can be organized using clean architecture, reusable page objects, realistic system-under-test design, and automated CI/CD workflows.

The project intentionally emphasizes engineering best practices over test quantity. By combining browser automation, API testing, a realistic FastAPI Mock Application, Docker, GitHub Actions, and scalable project organization, it provides a practical foundation for enterprise-quality automation development.

As the framework evolves beyond v1.0, future work will focus on Kubernetes-based execution, expanded browser coverage, advanced automation capabilities, and cloud-native testing while preserving the maintainability and extensibility established in this initial release.

## PETF v1.1 Configuration and Diagnostics

The Q4-S1 implementation checkpoint includes deterministic configuration,
environment selection, session-scoped API fixtures, isolated UI outputs,
failure diagnostics, screenshots, traces, and verified CI artifact staging.
This checkpoint is **not** a PETF v1.1.0 release declaration.

Operational references:

- [Configuration and environment selection](docs/testing/base-url-resolution.md)
- [Artifact directory contract](docs/architecture/artifact-directory-contract.md)
- [Screenshot hygiene](docs/screenshot-artifact-hygiene.md)
- [Trace activation](docs/trace-activation-policy.md)
- [CI artifact publication](docs/operations/ci-artifact-publication.md)
