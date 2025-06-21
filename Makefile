# Makefile for KeySentinel

# --- Targets that are not real files/directories ---
.PHONY: install-dev lint format check-format pre-commit-install pre-commit-test test coverage-html coverage-term clean

# --- Dev Environment Setup ---

# Install all development dependencies (from pyproject.toml)
install-dev:
	uv sync --all-extras

# --- Code Quality and Formatting ---

# Run Ruff linter on the source and tests to detect code issues
lint:
	ruff check keysentinel tests

# Automatically format code with Ruff
format:
	ruff format keysentinel tests

# Check if the code is already correctly formatted (no changes made)
check-format:
	ruff format --check keysentinel tests

# --- Git Hooks (Pre-commit) ---

# Install pre-commit hooks
pre-commit-install:
	pre-commit install

# Run all pre-commit checks on the current codebase
pre-commit-test:
	pre-commit run --all-files

# --- Testing ---

# Basic test run (includes coverage display in terminal)
test:
	pytest

# Run tests and generate a detailed HTML coverage report
coverage-html:
	pytest --cov=keysentinel --cov-report=html
	@echo "Open htmlcov/index.html to view the report."

# Run tests and show a simple terminal coverage report
coverage-term:
	pytest --cov=keysentinel --cov-report=term-missing

# --- Cleaning ---

# Clean up build artifacts, cache files, and test outputs
clean:
	rm -rf build dist *.egg-info htmlcov .pytest_cache .coverage

build:
	rm -rf build dist *.egg-info
	python -m build

release: build
	git add -A
	git diff --cached --quiet || git commit -m "Release v$(TAG)"
	git tag v$(TAG)
	git push origin v$(TAG)
	git push origin main
	@echo "Release v$(TAG) created and pushed."
