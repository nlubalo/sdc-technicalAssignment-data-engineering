# Setting up docker
docker-create-network:
	docker network create etl_network
# or hardcode the network name from the YAML file
# docker network create etl_network

docker-build:
	docker-compose build



docker-spin-up:
#docker-compose --env-file ./.env  up
	docker-compose -f docker-compose.yml --env-file ./.env up

#docker-compose --env-file ./.env -f ./docker-compose.yml up -d


#docker compose --env-file ./env up --build -d


docker-spin: docker-build docker-spin-up

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