install:
	python -m pip install --upgrade pip &&\
		python -m pip install -r requirements.txt

setup_db:
	alembic upgrade head

lint:
	python -m ruff check

format:
	python -m ruff format 

test:
	python -m pytest -v tests/

all: install setup_db lint test format