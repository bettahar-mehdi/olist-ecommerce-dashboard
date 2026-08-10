# Docker Deployment Guide for Olist E-Commerce Dashboard
.PHONY: help build run stop restart logs shell clean deploy

# Variables
IMAGE_NAME = olist-dashboard
CONTAINER_NAME = olist-dashboard
PORT = 8050

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

build: ## Build the Docker image
	docker build -t $(IMAGE_NAME) .

run: ## Run the container
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8050 $(IMAGE_NAME)

stop: ## Stop the container
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

restart: stop run ## Restart the container

logs: ## View container logs
	docker logs -f $(CONTAINER_NAME)

shell: ## Open a shell inside the container
	docker exec -it $(CONTAINER_NAME) /bin/bash

clean: ## Remove image and container
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

deploy: build run ## Build and deploy

status: ## Check container status
	docker ps -a --filter name=$(CONTAINER_NAME)
