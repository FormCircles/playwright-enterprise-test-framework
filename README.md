# SDET Playwright Portfolio (Python)

A comprehensive SDET portfolio focused on quality engineering at scale. Demonstrates Playwright (Python) automation frameworks, API testing, CI/CD pipelines, containerized execution with Docker, Kubernetes-based test orchestration, and real-world test strategy and architecture decisions.

A professional-grade SDET portfolio demonstrating API and UI automation using Python + Playwright, structured to reflect real-world enterprise test architecture.

![CI](https://github.com/Joseph-Doan/sdet-playwright-porfolio/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

## Table of Contents

1. Overview
2. Philosophy
3. Tech Stack
4. Repository Structure
5. Getting Started
6. Projects
7. Contributing
8. License

---

## 👋 Overview

This repository serves as a portfolio landing page for my work as a Software Development Engineer in Test (SDET).

Rather than focusing on isolated test scripts, this portfolio emphasizes:
- Test automation architecture and design
- Automation strategy and trade-offs
- Reliability, scalability, and maintainability
- Integration with real-world CI/CD pipelines
- Infrastructure-aware test execution

---

## 🧠 SDET Philosophy

Quality is engineered through reliable feedback, trustworthy automation, and reduced production risk.

---

## 🧰 Technology Stack

- Python
- Playwright
- pytest
- GitHub Actions
- Docker
- Kubernetes

---

## 📁 Repository Structure

See repository layout and framework organization.

---

## 📦 Projects

### ui-tests
Playwright UI automation framework.

### api-tests
API automation framework.

### ci-cd-pipelines
CI/CD automation workflows.

### docker-test-runner
Dockerized execution environments.

### kubernetes-test-jobs
Kubernetes orchestration examples.

### quality-engineering-docs
Quality strategy documentation.

---

## 🚀 Getting Started

Clone repository, create virtual environment, install dependencies, and execute tests.

---

## 🧪 Test Execution Guide

This repository contains API and UI automation frameworks executed independently to mirror enterprise CI/CD practices.

---

## 🧠 Key Design Decisions

- Service Layer
- Page Object Model
- Fixtures
- Behavior-Based Assertions
- Unified Playwright toolchain

---

## CI Test Execution

This project uses GitHub Actions to execute automated tests in CI.

### Traditional Pipeline Flow

1. Check out repository and submodules
2. Set up Python 3.12
3. Install framework and FastAPI application dependencies
4. Build Docker image
5. Publish image to GHCR
6. Pull published image
7. Run container
8. Wait for health check
9. Execute smoke tests
10. Capture diagnostics
11. Cleanup container

### Generated Artifacts

- test-results/results.xml
- test-results/report.html
- FastAPI runtime logs

### Why this Design

Provides repeatable execution, reusable artifacts, deployment validation, and enterprise-style CI/CD practices.

---

## Containerized CI Test Execution Flow

### Workflow Overview

```text
GitHub Actions
    ↓
Build Docker Image
    ↓
Publish Image to GHCR
    ↓
Pull Published Image
    ↓
Run Container
    ↓
Wait for Health Check
    ↓
Execute Smoke Tests
    ↓
Capture Logs on Failure
    ↓
Stop and Remove Container
```

### Container Publish Workflow

The container-publish workflow:

- Builds the FastAPI mock application image
- Validates the image
- Authenticates to GHCR
- Publishes the tested image

Published image:

ghcr.io/joseph-doan/fc-fastapi-sut:latest

### Container Run Workflow

The container-run workflow:

- Pulls the published image
- Starts the container
- Waits for health validation
- Executes smoke tests
- Captures diagnostics on failure
- Removes the container

### Runtime Configuration

Environment variables:

- IMAGE_NAME
- CONTAINER_NAME
- HOST_PORT
- CONTAINER_PORT
- BASE_URL

### Health Check Validation

The workflow waits for the `/health` endpoint to respond before executing tests.

### Smoke Test Execution

```bash
pytest -m smoke --base-url=$BASE_URL
```

### Failure Diagnostics

Automatically captures:

- docker ps -a
- docker logs

### Cleanup

```bash
docker stop $CONTAINER_NAME || true
docker rm $CONTAINER_NAME || true
```

### Enterprise CI/CD Mapping

| FormCircles Workflow | Enterprise Equivalent |
|---------------------|----------------------|
| GitHub Actions | Jenkins |
| GHCR | JFrog Artifactory |
| Docker Image | Deployable Artifact |
| Health Check | Deployment Validation |
| Smoke Tests | Post-Deployment Verification |
| Container Logs | Failure Diagnostics |
| Cleanup | CI Lifecycle Management |

### Current CI Capability

- Docker image creation
- Artifact publication
- Registry-based artifact reuse
- Health validation
- Smoke testing
- Failure diagnostics
- Automated cleanup
- Parameterized runtime configuration

---

## 🎯 How to Use This Portfolio

- Hiring managers: review project documentation
- SDETs: use as a framework reference
- Interviewers: discuss architecture and quality strategy

---

## ⭐ Why This Project Matters

Demonstrates:

- Real-world SDET architecture
- Scalable test design
- Maintainable automation
- Strong debugging skills

---

## 🤝 Contributing

Suggestions and improvements are welcome.

---

## 📄 License

MIT License.

---

## 📬 Contact

GitHub: https://github.com/Joseph-Doan
