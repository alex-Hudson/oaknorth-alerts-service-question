VERSION ?= 1.0.1

build:
	VERSION=$(VERSION) docker compose build

run:
	VERSION=$(VERSION) docker compose up

clean:
	docker compose down

format:
	poetry run black .
	poetry run isort .

test:
	poetry run pytest tests

help:
	@echo "build - Build the docker image"
	@echo "run - Start the services + PostgreSQL in docker compose"
	@echo "clean - Stop and remove the services"
	@echo "format - Format the code with black and isort"
	@echo "test - Run all tests. Requires Docker to be running."

.PHONY: build run clean format test help