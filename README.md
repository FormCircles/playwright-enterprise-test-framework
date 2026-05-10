# SDET Playwright Portfolio (Python)

A comprehensive SDET portfolio focused on quality engineering at scale. Demonstrates Playwright (Python) automation frameworks, API testing, CI/CD pipelines, containerized execution with Docker, Kubernetes-based test orchestration, and real-world test strategy and architecture decisions.

A professional-grade SDET portfolio demonstrating API and UI automation using Python + Playwright, structured to reflect real-world enterprise test architecture.


![CI](https://github.com/Joseph-Doan/sdet-playwright-porfolio/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Table of Contents

1. [Overview](#overview)
2. [Philosophy](#philosophy)
3. [Tech Stack](#tech-stack)
4. [Repository Structure](#repository-structure)
5. [Getting Started](#getting-started)
6. [Projects](#projects)
7. [Contributing](#contributing)
8. [License](#license)

---

## 👋 Overview

This repository serves as a **portfolio landing page** for my work as a Software Development Engineer in Test (SDET).

Rather than focusing on isolated test scripts, this portfolio emphasizes:
- Test automation **architecture and design**
- Automation **strategy and trade-offs**
- Reliability, scalability, and maintainability
- Integration with **real-world CI/CD pipelines**
- Infrastructure-aware test execution

The goal is to demonstrate **how quality is engineered**, not just how tests are written.

---

## 🧠 SDET Philosophy

I view the SDET role as an **engineering discipline that enables teams to ship with confidence**.

Quality is not defined by the number of tests written, but by:
- The **speed and reliability of feedback**
- The **trustworthiness of automation**
- The **reduction of production risk**

Automation should protect critical user and business flows, integrate seamlessly into CI/CD, and scale as systems grow.  
Flaky or low-signal tests are treated as system problems, not acceptable trade-offs.

---

## 🧰 Technology Stack

- **Language:** Python  
- **UI & API Automation:** Playwright  
- **Test Runner:** pytest  
- **CI/CD:** GitHub Actions  
- **Containerization:** Docker  
- **Test Orchestration:** Kubernetes  

Tooling choices are driven by **stability, observability, and scalability**, not popularity.

---


## 📁 Repository Structure

This repository acts as a portfolio landing page and index for multiple focused projects:

```Repository Structure
playwright-enterprise-test-framework/
│
├── api-tests/                 # API test suite
│   ├── services/             # Service layer (business logic)
│   ├── tests/                # API test cases
│   └── conftest.py           # API fixtures
│
├── ui-tests/                 # UI test suite
│   ├── pages/                # Page Object Models
│   └── tests/                # UI test cases
│
├── core/                     # Shared framework components
│   ├── api/                  # API client
│   ├── config/               # Environment & settings
│   ├── fixtures/             # Base fixtures
│   └── logging/              # Logging utilities
│
├── infra/                    # Infrastructure (CI/CD, Docker)
├── test-data/                # Test data
├── reports/                  # Test reports
└── pytest.ini
```


---

## 📦 Projects

### 🔹 ui-tests
A Playwright-based UI automation framework using Python and pytest.

**Highlights:**
- Page Object Model
- Parallel execution
- Test tagging (smoke, regression)
- Flakiness mitigation strategies
- Failure artifacts (screenshots, videos)

---

### 🔹 api-tests
An API automation framework using Playwright’s request context.

**Highlights:**
- CRUD API testing
- Authentication handling
- Schema validation
- Data-driven testing
- Test pyramid alignment

---

### 🔹 ci-cd-pipelines
CI/CD configurations demonstrating how automated tests integrate into real delivery workflows.

**Highlights:**
- Pull request validation
- Regression runs on merge
- Test artifact publishing
- Tag-based test selection

---

### 🔹 docker-test-runner
Dockerized test execution environments for consistent local and CI runs.

**Highlights:**
- Reproducible environments
- Faster onboarding
- Separation of test and host dependencies

---

### 🔹 kubernetes-test-jobs
Kubernetes manifests for scalable and parallel test execution.

**Highlights:**
- Kubernetes Jobs for test runs
- Parallel pod execution
- Environment configuration via ConfigMaps
- Clear guidance on when Kubernetes is appropriate vs overkill

---

### 🔹 quality-engineering-docs
Documentation focused on quality leadership and strategy.

**Includes:**
- Test strategy
- Risk-based testing
- Automation ROI
- Test metrics and reporting
- Example test plans

---
## 🚀 Getting Started

1. Clone this repo
   ```bash
   git clone https://github.com/YOUR_USERNAME/playwright-enterprise-test-framework.git
   cd playwright-enterprise-test-framework
   ```
2. Create virtual environment
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate     #Windows
   ```
3. Install dependencies
   ```bash
   pip install -r requirements
   playwright install
   ```
4. Running Tests
   Run all tests
   ```bash
   pytest -v
   ```
5. Run API tests only
   ```bash
   pytest api-tests -v
   ```
6. Run UI tsts only
   ```bash
   pytst ui-tests --headed -v
   ```
---

## 🧪 Test Execution Guide

This repository contains two independent automation frameworks:

- API Automation Framework (Playwright Request API)

- UI Automation Framework (Playwright Browser + POM)

These test suites are intentionally executed separately to mirror real-world CI/CD pipeline stages and to prevent event loop conflicts.

⚠️ Note: The FastAPI mock service used by this framework is maintained in the `sut/FastAPIMockApp` submodule. Docker startup and health validation instructions are documented in the FastAPIMockApp repository README. The FastAPI mock backend must be running locally on http://localhost:8080.

### 🚀 Run API Tests

What this covers:

- Authentication

- CRUD operations

- Negative scenarios

- Validation errors

- Authorization checks

### 🖥 Run UI Tests

What this covers:

- Login success

- Login failure

- Devices page rendering

- Page Object Model structure

## 🧠 Why Separate Execution?

In production-grade automation:

- API and UI tests run in separate CI stages

- API tests are fast and validate business logic

- UI tests validate user workflows

- Separation avoids async loop conflicts and reduces pipeline instability

This architecture mirrors real enterprise automation strategy.

---
## 🧠 Key Design Decisions

🔹 Service Layer (API)

Encapsulates API logic for better reusability and maintainability.

🔹 Page Object Model (UI)

Separates UI structure from test logic.

🔹 Fixtures

Reusable setup for:

- API clients

- Base URLs

- Test configuration

🔹 Behavior-Based Assertions

🔹 Why Playwright for API Testing?

Using Playwright for both API and UI testing allows a single unified toolchain, shared configuration, and consistent CI execution. This mirrors how modern SDET teams reduce tooling fragmentation in real-world environments.

Tests validate actual system behavior instead of fragile UI text.

---

## CI Test Execution

This project uses GitHub Actions to execute automated tests in CI.

### Pipeline flow
1. Check out repository and submodules
2. Set up Python 3.12
3. Install framework and FastAPI application dependencies
4. Start the FastAPI mock application
5. Wait for the API to become ready
6. Execute pytest-based automated tests
7. Upload test results and server logs as artifacts

### Generated artifacts
- `test-results/results.xml` — JUnit XML test results
- `test-results/report.html` — HTML pytest report
- `sut/FastAPIMockApp/server.log` — FastAPI startup/runtime log

### Why this design
This pipeline is structured to provide repeatable automated test execution, useful debugging artifacts, and a cleaner CI flow aligned with enterprise quality engineering practices.

---

## 🎯 How to Use This Portfolio

- Hiring managers: Review the README files inside each project to understand architecture and reasoning
  
- SDETs: Use this as a reference for building scalable automation systems
  
- Interviewers: Treat this portfolio as a discussion starter for system design and quality strategy

---
## ⭐ Why This Project Matters

This framework demonstrates:

-  Real-world SDET architecture

-  Scalable test design

-  Maintainable automation practices

-  Strong debugging and problem-solving skills


## 🤝 Contributing

Suggestions and improvements are welcome.
Please open an issue or pull request with a clear description of proposed changes.

---

## 📄 License

This project is licensed under the MIT License.
See the LICENSE file for details.

---


## 📬 Contact

GitHub: https://github.com/Joseph-Doan

LinkedIn: (add your LinkedIn profile here)
