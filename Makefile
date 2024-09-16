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
migrate:
	docker exec backend alembic upgrade head

# Commands for delete data
clean:
	$(DOCKER_COMPOSE) down --volumes --remove-orphans