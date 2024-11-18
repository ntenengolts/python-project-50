lint:
	poetry run flake8 .
	poetry run isort --check .


install:
	poetry install


test-coverage:
	poetry run pytest --cov=gendiff --cov-report=term-missing
