.PHONY: help build deploy test clean

help:
	@echo "Available commands:"
	@echo "  make build   - Build the SAM application"
	@echo "  make deploy  - Deploy the application to AWS"
	@echo "  make test    - Run local tests"
	@echo "  make clean   - Clean build artifacts"

build:
	sam build

deploy:
	sam deploy --guided

deploy-fast:
	sam deploy

test:
	python -m pytest tests/ -v

local-api:
	sam local start-api

clean:
	rm -rf .aws-sam/
