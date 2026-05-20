.PHONY: help setup backend-setup mobile-setup docker-up docker-down backend-run backend-test mobile-run mobile-test format lint clean

help:
	@echo "UstaadX Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup          - Complete project setup"
	@echo "  make backend-setup  - Setup backend only"
	@echo "  make mobile-setup   - Setup mobile only"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up      - Start Docker services"
	@echo "  make docker-down    - Stop Docker services"
	@echo ""
	@echo "Development:"
	@echo "  make backend-run    - Run backend server"
	@echo "  make backend-test   - Run backend tests"
	@echo "  make mobile-run     - Run mobile app"
	@echo "  make mobile-test    - Run mobile tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         - Format all code"
	@echo "  make lint           - Lint all code"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Clean build artifacts"

setup: backend-setup mobile-setup
	@echo "✓ Complete setup finished"

backend-setup:
	@echo "Setting up backend..."
	cd apps/backend_api && cp .env.example .env
	cd apps/backend_api && python -m venv venv
	cd apps/backend_api && . venv/bin/activate && pip install -r requirements.txt
	@echo "✓ Backend setup complete"

mobile-setup:
	@echo "Setting up mobile app..."
	cd apps/mobile_app && cp .env.example .env
	cd apps/mobile_app && flutter pub get
	@echo "✓ Mobile setup complete"

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "✓ Docker services started"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down
	@echo "✓ Docker services stopped"

backend-run:
	@echo "Starting backend server..."
	cd apps/backend_api && . venv/bin/activate && uvicorn app.main:app --reload

backend-test:
	@echo "Running backend tests..."
	cd apps/backend_api && . venv/bin/activate && pytest

mobile-run:
	@echo "Running mobile app..."
	cd apps/mobile_app && flutter run

mobile-test:
	@echo "Running mobile tests..."
	cd apps/mobile_app && flutter test

format:
	@echo "Formatting code..."
	cd apps/backend_api && . venv/bin/activate && black app/
	cd apps/mobile_app && flutter format lib/
	@echo "✓ Code formatted"

lint:
	@echo "Linting code..."
	cd apps/backend_api && . venv/bin/activate && ruff check app/
	cd apps/mobile_app && flutter analyze
	@echo "✓ Linting complete"

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd apps/mobile_app && flutter clean
	@echo "✓ Cleanup complete"
