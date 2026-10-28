# Enterprise MLOps Platform

An end-to-end, production-ready MLOps reference architecture demonstrating the full lifecycle of machine learning models—from experiment tracking to declarative GitOps deployments on Kubernetes.

## 🎯 Architecture Overview

This repository bridges the gap between Data Science and Platform Engineering. It implements a fully automated CI/CD/CT (Continuous Training) pipeline that ensures models are rigorously tested, registered, and deployed with zero-downtime using modern cloud-native standards.

### Core Stack
* **Experiment Tracking & Registry:** MLflow
* **Model Serving:** FastAPI (Containerized REST API)
* **Infrastructure as Code (IaC):** Terraform
* **Container Orchestration:** Kubernetes (AKS)
* **GitOps Delivery:** Argo CD / Flux CD
* **Secret Management:** External Secrets Operator (Zero-Trust)
* **CI/CD Quality Gates:** GitHub Actions (Linting, Security Scans, Model Validation)

## 📂 Repository Structure

Our monorepo is structured following Platform Engineering best practices:

```text
├── .github/workflows/   # Automated CI pipelines (Training validation, Image build, GitOps PRs)
├── docs/adr/            # Architecture Decision Records (ADRs)
├── gitops/              # Declarative K8s manifests (Helm values, ApplicationSets)
│   ├── apps/            # Inference APIs and model endpoints
│   └── platform/        # MLflow Server, Prometheus, Grafana
├── infra/               # Terraform modules for base infrastructure provisioning
├── scripts/             # Python-based pre-commit hooks and structural validators
├── src/                 
│   ├── training/        # ML model training scripts instrumented with MLflow
│   └── serving/         # FastAPI wrappers for low-latency model inference
└── tests/               # Unit, integration, and data drift tests


🛡️ Production Standards & Security
Inspired by enterprise GitOps workflows, this platform enforces strict quality gates:

Mechanical Promotion: CI pipelines never deploy directly to the cluster. They build immutable artifacts and open automated Pull Requests updating the image.tag in the gitops/ directory.

Zero-Trust Secrets: No credentials exist in the codebase. Pods retrieve remote secrets dynamically via ClusterSecretStore.

Security Scans: Trivy container scanning, SBOM generation, and Gitleaks ensure secure builds before promotion.

Gateway API: Exposure is managed via unified Gateways with dynamic TLS termination, avoiding ingress-controller sprawl.


🚀 Getting Started
Developer Experience (DX) via Makefile:

make dev-up: Spins up the local MLflow Tracking Server and Postgres backend via Docker Compose.

make train: Executes the local training script and logs metrics to MLflow.

make serve: Builds the inference API container and serves it locally on port 8000.

make test: Runs pytest and structural compliance checks (scripts/validate_manifests.py).