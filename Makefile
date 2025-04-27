# Define compose files
COMPOSE_FILES = -f docker-compose.yml -f docker-compose.mongo.yml

# Up services
up:
	docker-compose $(COMPOSE_FILES) up

# Up and build
up-build:
	docker-compose $(COMPOSE_FILES) up --build

# Down services
down:
	docker-compose $(COMPOSE_FILES) down

# Rebuild services
build:
	docker-compose $(COMPOSE_FILES) build

# Show logs
logs:
	docker-compose $(COMPOSE_FILES) logs -f --tail=100

# Prune dangling docker volumes (optional)
prune:
	docker volume prune -f
