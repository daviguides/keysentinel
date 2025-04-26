# Makefile for KeySentinel

.PHONY: install-dev lint format check-format pre-commit-install

install-dev:
	uv sync --all-extras

lint:
	ruff check keysentinel

format:
	ruff format keysentinel

check-format:
	ruff format --check keysentinel

pre-commit-install:
	pre-commit install

pre-commit-test:
	pre-commit run --all-files