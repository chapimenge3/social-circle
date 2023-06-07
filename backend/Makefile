# Helper makefile for social circle project

run:
	@echo "Running docker for social circle project"
	@echo "Make sure to build the containers before running this command"
	docker compose up -d

start:
	@echo "Starting docker for social circle project"
	@echo "Make sure to build the containers before running this command"
	docker compose up -d --build

restart:
	@echo "Restarting docker for social circle project"
	@echo "Make sure to build the containers before running this command"
	docker compose restart

stop:
	@echo "Stopping docker for social circle project"
	docker compose down

makemigrations:
	@echo "Making migrations for social circle project"
	@echo "Make sure to run the server before running this command"
	./manage.py makemigrations

migrate:
	@echo "Migrating for social circle project"
	@echo "Make sure to run the server before running this command"
	docker compose exec web python manage.py migrate

createsuperuser:
	@echo "Creating superuser for social circle project"
	@echo "Make sure to run the server before running this command"
	docker compose exec web python manage.py createsuperuser

create-app:
	@echo "Creating app for social circle project"
	@echo "Make sure to run the server before running this command"
	./manage.py startapp $(name)

shell:
	@echo "Opening shell for social circle project"
	@echo "Make sure to run the server before running this command"
	docker compose exec web python manage.py shell

test:
	@echo "Running tests for social circle project"
	docker compose exec web python manage.py test

lint:
	@echo "Running lint for social circle project"
	docker compose exec web flake8

logs:
	@echo "Showing logs for social circle project"
	docker compose logs -f

ps:
	@echo "Showing containers for social circle project"
	docker compose ps

build:
	@echo "Building containers for social circle project"
	docker compose build

build-no-cache:
	@echo "Building containers for social circle project"
	docker compose build --no-cache

build-nc:
	@echo "Building containers for social circle project"
	docker compose build --no-cache