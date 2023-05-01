# Setting up docker

docker-build:
	docker-compose build

docker-init:
	docker-compose up airflow-init


up:
	docker-compose -f docker-compose.yml --env-file ./.env up


down:
	docker compose down

#####################################
# Tresting, auto formating, type checks, and linting checks
pytest:
	docker exec webserver pytest -p no:warnings -v /opt/airflow/tests

format:
	docker exec webserver python -m black -S --line-length 79 .

isort:
	docker exec webserver isort .

type:
	docker exec webserver mypy --ignore-missing-imports /opt/airflow

lint:
	docker exec webserver flake8 /opt/airflow/dags

ci: isort format type lint pytest

################################################################################

# Create tables in Warehouse
spectrum-migration:
	./spectrum_migrate.sh

db-migration:
	@read -p "Enter migration name:" migration_name; docker exec webserver yoyo new ./migrations -m "$$migration_name"