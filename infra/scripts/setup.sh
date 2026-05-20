#!/bin/bash

# UstaadX Setup Script
# This script sets up the complete development environment

set -e

echo "========================================="
echo "UstaadX Development Environment Setup"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print colored message
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

# Check prerequisites
echo "Checking prerequisites..."
echo ""

MISSING_DEPS=0

if command_exists docker; then
    print_success "Docker installed"
else
    print_error "Docker not found"
    MISSING_DEPS=1
fi

if command_exists docker-compose; then
    print_success "Docker Compose installed"
else
    print_error "Docker Compose not found"
    MISSING_DEPS=1
fi

if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION installed"
else
    print_error "Python 3 not found"
    MISSING_DEPS=1
fi

if command_exists flutter; then
    FLUTTER_VERSION=$(flutter --version | head -n1 | cut -d' ' -f2)
    print_success "Flutter $FLUTTER_VERSION installed"
else
    print_warning "Flutter not found (optional for backend-only development)"
fi

if command_exists git; then
    print_success "Git installed"
else
    print_error "Git not found"
    MISSING_DEPS=1
fi

echo ""

if [ $MISSING_DEPS -eq 1 ]; then
    print_error "Missing required dependencies. Please install them and try again."
    exit 1
fi

# Setup backend
echo "========================================="
echo "Setting up Backend"
echo "========================================="
echo ""

cd apps/backend_api

if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    print_success ".env file created"
else
    print_warning ".env file already exists, skipping"
fi

if [ ! -d venv ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists, skipping"
fi

echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
print_success "Python dependencies installed"

cd ../..

# Setup mobile app
if command_exists flutter; then
    echo ""
    echo "========================================="
    echo "Setting up Mobile App"
    echo "========================================="
    echo ""

    cd apps/mobile_app

    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        print_success ".env file created"
    else
        print_warning ".env file already exists, skipping"
    fi

    echo "Installing Flutter dependencies..."
    flutter pub get > /dev/null 2>&1
    print_success "Flutter dependencies installed"

    cd ../..
fi

# Setup Docker
echo ""
echo "========================================="
echo "Setting up Docker Services"
echo "========================================="
echo ""

echo "Starting Docker services..."
docker-compose up -d

echo "Waiting for services to be ready..."
sleep 5

if docker-compose ps | grep -q "Up"; then
    print_success "Docker services started"
else
    print_error "Failed to start Docker services"
    exit 1
fi

# Run migrations
echo ""
echo "========================================="
echo "Running Database Migrations"
echo "========================================="
echo ""

cd apps/backend_api
source venv/bin/activate

echo "Initializing Alembic..."
alembic revision --autogenerate -m "Initial migration" > /dev/null 2>&1 || true

echo "Running migrations..."
alembic upgrade head
print_success "Database migrations complete"

cd ../..

# Final instructions
echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the backend:"
echo "   cd apps/backend_api"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Start Celery worker (in another terminal):"
echo "   cd apps/backend_api"
echo "   source venv/bin/activate"
echo "   celery -A app.core.celery_app worker --loglevel=info"
echo ""

if command_exists flutter; then
    echo "3. Run the mobile app (in another terminal):"
    echo "   cd apps/mobile_app"
    echo "   flutter run"
    echo ""
fi

echo "4. Access the API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "5. Check health endpoint:"
echo "   curl http://localhost:8000/health"
echo ""
echo "For more information, see docs/setup_guide.md"
echo ""
