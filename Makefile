.PHONY: help install format lint test dev-up dev-down train serve clean

# Configurações do Ambiente
VENV_NAME ?= .venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

help: ## Mostra os comandos disponíveis neste Makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Cria o ambiente virtual e instala dependências de treino, serving e dev
	python3 -m venv $(VENV_NAME)
	$(PIP) install --upgrade pip
	$(PIP) install -r src/training/requirements.txt
	$(PIP) install -r src/serving/requirements.txt
	$(PIP) install pytest black ruff isort

format: ## Formata o código fonte com Black e Isort
	$(VENV_NAME)/bin/black src/ tests/ scripts/
	$(VENV_NAME)/bin/isort src/ tests/ scripts/

lint: ## Verifica a qualidade do código e detecta bad practices com Ruff
	$(VENV_NAME)/bin/black --check src/ tests/ scripts/
	$(VENV_NAME)/bin/ruff check src/ tests/ scripts/

test: ## Roda testes unitários e valida a estrutura e segurança dos manifestos GitOps
	$(VENV_NAME)/bin/pytest tests/
	$(PYTHON) scripts/validate_manifests.py

dev-up: ## Sobe a infraestrutura local (MLflow Tracking Server + Postgres backend) via Docker Compose
	docker-compose -f infra/local/docker-compose.yml up -d

dev-down: ## Derruba a infraestrutura local do MLflow
	docker-compose -f infra/local/docker-compose.yml down

train: ## Executa o script de treino registrando as métricas no MLflow local
	MLFLOW_TRACKING_URI=http://localhost:5000 $(PYTHON) src/training/train.py

serve: ## Constrói e sobe a API de inferência na porta 8000
	docker build -t inference-api:local -f src/serving/Dockerfile src/serving/
	docker run -p 8000:8000 \
		--network local_default \
		--env MLFLOW_TRACKING_URI=http://mlflow:5000 \
		--env MODEL_RUN_ID=$(RUN_ID) \
		inference-api:local

clean: ## Remove o ambiente virtual, caches do Python e do pytest
	rm -rf $(VENV_NAME)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +