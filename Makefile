install:
	python -m pip install --upgrade pip &&\
		python -m pip install -r requirements.txt

migrations:
	python -m alembic revision --autogenerate -m "$(slug)"

migrate:
	python -m alembic upgrade head

lint:
	python -m ruff check

format:
	python -m ruff format 

test:
	python -m pytest -v tests/

init_database: 
	make migrations slug="inti_database" &&\
		make migrate 

all: install lint test format