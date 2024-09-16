# Variables
DOCKER_COMPOSE = docker compose

# Commands
up:
	$(DOCKER_COMPOSE) up
down:
	$(DOCKER_COMPOSE) down
build:
	$(DOCKER_COMPOSE) build
logs:
	$(DOCKER_COMPOSE) logs -f

# Migration commands
make_migration:
	docker exec backend alembic revision --autogenerate -m "$(msg)"

migrate:
	docker exec backend alembic upgrade head