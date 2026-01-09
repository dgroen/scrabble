SHELL := /bin/bash

.PHONY: help venv install run-example run-demo tox

help:
	@echo "Makefile targets:"
	@echo "  make venv         # create virtualenv (uses uv if available, otherwise .venv)"
	@echo "  make install      # install dependencies (uses uv if available, otherwise pip)"
	@echo "  make run-example  # run example.py using the project venv or uv"
	@echo "  make run-demo     # run example_game_session.py using the project venv or uv"
	@echo "  make tox          # run tox (uses uv when available, otherwise local python)"

venv:
	@if command -v uv >/dev/null 2>&1; then \
		echo "uv detected — please use your preferred uv command to create and manage the venv (examples in README)"; \
		exit 0; \
	else \
		python -m venv .venv && .venv/bin/python -m pip install --upgrade pip; \
		echo "Created .venv and upgraded pip."; \
	fi

install: venv
	@if command -v uv >/dev/null 2>&1; then \
		echo "uv detected — run 'uv install' (or consult uv docs) to install project dependencies into the uv-managed env."; \
		exit 0; \
	else \
		. .venv/bin/activate && pip install -e '.[dev]' || pip install -r dev-requirements.txt; \
	fi

run-example:
	@if command -v uv >/dev/null 2>&1; then \
		echo "uv detected — run the example inside uv (e.g. 'uv run python example.py')"; \
	else \
		. .venv/bin/activate && python example.py; \
	fi

run-demo:
	@if command -v uv >/dev/null 2>&1; then \
		echo "uv detected — run the demo inside uv (e.g. 'uv run python example_game_session.py')"; \
	else \
		. .venv/bin/activate && python example_game_session.py; \
	fi

tox:
	@if command -v uv >/dev/null 2>&1; then \
		echo "uv detected — run tox inside uv-managed env (e.g. 'uv run tox -e py')"; \
	else \
		. .venv/bin/activate && python -m tox $(filter-out $@,$(MAKECMDGOALS)); \
	fi
