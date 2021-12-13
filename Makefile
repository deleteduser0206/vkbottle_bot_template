# Treat these arguments not as files, but as recipes
.PHONY: run venv install install-dev update githooks pre-commit check fix

# Used to execute all in one shell
.ONESHELL:

# Default recipe
DEFAULT: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Use poetry or activated venv
interpreter := $(shell poetry env info --path > /dev/null 2>&1 && echo "poetry run")


check-venv:
	$(if $(interpreter),, $(error No poetry environment found, either run "make venv"))

run: check-venv ## Run bot
	@$(interpreter) python -m src

venv: ## Create virtual environment
	@python -m pip install poetry
	@poetry env use python
	echo; echo "Poetry created virtual environment"

install:  ## Install only prod dependencies
	@poetry install
	echo; echo "Installed only prod dependencies"

install-dev: ## Install prod & dev dependencies
	@poetry install
	echo; echo "Installed prod & dev dependencies"

update: ## Update dependencies
	@poetry install
	echo; echo "Dependencies updated"

githooks: check-venv  ## Install git hooks
	@$(interpreter) pre-commit install

pre-commit: check-venv ## Run pre-commit
	@$(interpreter) pre-commit run

check: check-venv ## Run pre-commit
	@$(interpreter) pre-commit run

fix: check-venv ## Run pre-commit
	@$(interpreter) pre-commit run