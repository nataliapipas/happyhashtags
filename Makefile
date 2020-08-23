.DOCKER_COMPOSE := docker-compose -f docker-compose-dev.yml

setup: build wait-for-it migrate ## Setup project

.PHONY: build
build:
	$(.DOCKER_COMPOSE) pull && \
	$(.DOCKER_COMPOSE) up -d --build

.PHONY: up
up:
	$(.DOCKER_COMPOSE) up -d

.PHONY: down
down:
	$(.DOCKER_COMPOSE) down --remove-orphans

.PHONY: down-with-volumes
down-with-volumes:
	$(.DOCKER_COMPOSE) down --remove-orphans --volumes

.PHONY: logs
logs: ## Run logs
	$(.DOCKER_COMPOSE) logs -t -f --tail="all"

.PHONY: restart
restart:
	$(.DOCKER_COMPOSE) restart

.PHONY: wait-for-it
wait-for-it:
	until PGPASSWORD=hashtags psql -U happy -d happy_hashtags -h localhost -c "SELECT 1;" >/dev/null 2>&1; do sleep 1; done

.PHONY: migrate
migrate: ## Run the migrations
	$(.DOCKER_COMPOSE) exec hh /usr/local/bin/alembic upgrade head
