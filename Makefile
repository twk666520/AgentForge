
.PHONY: install test test-core test-ocr lint format check clean

install:
	pip install -e core/
	pip install -e skills/skill-ocr/

test-core:
	PYTHONPATH=core/src pytest core/tests/ -v

test-ocr:
	PYTHONPATH=core/src:skills/skill-ocr/src pytest skills/skill-ocr/tests/ -v

test: test-core test-ocr

lint:
	ruff check core/src/ skills/skill-ocr/src/

format:
	ruff format core/src/ skills/skill-ocr/src/

format-check:
	ruff format --check core/src/ skills/skill-ocr/src/

check: lint format-check test

clean:
	rm -rf .pytest_cache .ruff_cache __pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
