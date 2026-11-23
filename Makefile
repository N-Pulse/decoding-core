.PHONY: format lint typecheck test check diagram

diagram:
	classpy sync
	PLANTUML_LIMIT_SIZE=16384 plantuml -tpng docs/diagrams/*.puml

format:
	-poetry run docformatter src tests

lint:
	poetry run pylint src

typecheck:
	poetry run pyright src

test:
	-poetry run pytest

check: diagram format lint typecheck test
