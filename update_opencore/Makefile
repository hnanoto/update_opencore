.PHONY: help install test lint format clean build

# Variáveis
PYTHON = python3
PIP = pip3
PROJECT_NAME = update-opencore

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala as dependências do projeto
	$(PIP) install -e .
	$(PIP) install -e ".[dev]"

install-dev: ## Instala dependências de desenvolvimento
	$(PIP) install pre-commit
	pre-commit install

test: ## Executa os testes
	$(PYTHON) -m pytest tests/ -v

test-coverage: ## Executa os testes com cobertura
	$(PIP) install pytest-cov
	$(PYTHON) -m pytest tests/ --cov=. --cov-report=html --cov-report=term

lint: ## Executa verificações de qualidade de código
	@echo "Executando pylint..."
	$(PYTHON) -m pylint *.py --disable=C0114,C0115,C0116,R0903,R0913
	@echo "Executando flake8..."
	$(PYTHON) -m flake8 *.py --max-line-length=100 --extend-ignore=E203,W503
	@echo "Executando mypy..."
	$(PYTHON) -m mypy *.py --ignore-missing-imports

format: ## Formata o código usando black e isort
	$(PIP) install black isort
	$(PYTHON) -m black *.py --line-length=100
	$(PYTHON) -m isort *.py --profile=black

check-format: ## Verifica se o código está formatado corretamente
	$(PIP) install black isort
	$(PYTHON) -m black *.py --check --line-length=100
	$(PYTHON) -m isort *.py --check-only --profile=black

clean: ## Remove arquivos temporários e caches
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/
	rm -f *.log

build: ## Constrói o pacote
	$(PYTHON) -m build

check-all: format lint test ## Executa todas as verificações

run: ## Executa o script principal
	$(PYTHON) main.py

validate: ## Valida a sintaxe de todos os arquivos Python
	@echo "Validando sintaxe Python..."
	@for file in *.py; do \
		echo "Verificando $$file..."; \
		$(PYTHON) -m py_compile "$$file" || exit 1; \
	done
	@echo "Todos os arquivos Python têm sintaxe válida!"

security: ## Executa verificações de segurança
	$(PIP) install bandit
	$(PYTHON) -m bandit -r . -f json -o bandit-report.json || true
	@echo "Relatório de segurança salvo em bandit-report.json"

docs: ## Gera documentação
	$(PIP) install pdoc3
	$(PYTHON) -m pdoc --html --output-dir docs .

setup: install install-dev ## Configura o ambiente de desenvolvimento completo
