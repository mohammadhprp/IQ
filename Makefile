.PHONY: format install run clean build run stop help

help:
	@echo "Available commands:"
	@echo "  make format        - Format code using black"
	@echo "  make clean         - Clean up Python cache files"
	@echo "  make build         - Build Docker containers"
	@echo "  make run           - Run Docker containers"
	@echo "  make stop          - Stop Docker containers"
	@echo "  make help          - Show this help message" 

format:
	black .

build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".ruff_cache" -exec rm -r {} +
