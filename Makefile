.PHONY: format lint typecheck test check

format:
	-poetry run docformatter src tests

lint:
	poetry run pylint src

typecheck:
	poetry run pyright src

test:
	-poetry run pytest

check: format lint typecheck test
