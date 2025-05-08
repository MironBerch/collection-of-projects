.PHONY: check
check:
	uv run ruff check

.PHONY: format
format:
	uv run ruff format

.PHONY: build
build:
	touch .env
	uv sync --dev

.PHONY: run
run:
	uv run litestar --app=src.app:app run --reload