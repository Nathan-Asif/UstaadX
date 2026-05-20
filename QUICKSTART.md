# UstaadX Quick Start Guide

Get UstaadX up and running in minutes.

## Prerequisites

Install these before starting:

- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Flutter 3.19+** - [Download](https://flutter.dev/docs/get-started/install)
- **Git** - [Download](https://git-scm.com/downloads)

## Quick Setup

### Option 1: Automated Setup (Recommended)

#### Linux/Mac:
```bash
chmod +x infra/scripts/setup.sh
./infra/scripts/setup.sh
```

#### Windows:
```cmd
infra\scripts\setup.bat
```

### Option 2: Manual Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd ustaadx
```

#### 2. Start Docker Services
```bash
docker-compose up -d
```

#### 3. Setup Backend
```bash
cd apps/backend_api

# Copy environment file
cp .env.example .env

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

#### 4. Setup Mobile App
```bash
cd apps/mobile_app

# Copy environment file
cp .env.example .env

# Install dependencies
flutter pub get

# Generate code
flutter pub run build_runner build --delete-conflicting-outputs
```

## Running the Application

### Start Backend Server

```bash
cd apps/backend_api
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000

### Start Celery Worker (Optional)

In a new terminal:
```bash
cd apps/backend_api
source venv/bin/activate  # or venv\Scripts\activate on Windows
celery -A app.core.celery_app worker --loglevel=info
```

### Run Mobile App

In a new terminal:
```bash
cd apps/mobile_app
flutter run
```

## Verify Installation

### Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "UstaadX",
  "version": "v1",
  "environment": "development"
}
```

### Check API Documentation
Open in browser: http://localhost:8000/docs

### Check Database
```bash
docker-compose exec postgres psql -U ustaadx -d ustaadx_db -c "\dt"
```

### Check Redis
```bash
docker-compose exec redis redis-cli ping
```

## Common Commands

### Docker
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart backend
```

### Backend
```bash
# Run tests
pytest

# Format code
black app/

# Lint code
ruff check app/

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Mobile
```bash
# Run tests
flutter test

# Format code
flutter format lib/

# Analyze code
flutter analyze

# Generate code
flutter pub run build_runner build --delete-conflicting-outputs

# Clean build
flutter clean
```

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process using port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Connection Error
```bash
# Restart PostgreSQL
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

### Redis Connection Error
```bash
# Restart Redis
docker-compose restart redis

# Check logs
docker-compose logs redis
```

### Flutter Build Issues
```bash
cd apps/mobile_app
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

## Next Steps

1. **Read Documentation**
   - [Architecture Overview](docs/architecture.md)
   - [Setup Guide](docs/setup_guide.md)
   - [API Conventions](docs/api_conventions.md)

2. **Explore the Code**
   - Backend: `apps/backend_api/app/`
   - Mobile: `apps/mobile_app/lib/`
   - Docs: `docs/`

3. **Start Building**
   - Create a feature branch
   - Implement your feature
   - Write tests
   - Submit a PR

## Getting Help

- Check [Setup Guide](docs/setup_guide.md) for detailed instructions
- Review [Architecture Documentation](docs/architecture.md)
- Search existing issues on GitHub
- Create a new issue if needed

## Project Structure

```
ustaadx/
├── apps/
│   ├── backend_api/      # FastAPI backend
│   └── mobile_app/       # Flutter mobile app
├── packages/
│   └── shared_models/    # Shared data models
├── infra/
│   ├── docker/           # Docker configurations
│   └── scripts/          # Utility scripts
├── docs/                 # Documentation
├── .github/              # GitHub workflows
└── docker-compose.yml    # Docker Compose config
```

## Key Technologies

- **Backend**: FastAPI, PostgreSQL, Redis, Celery
- **Mobile**: Flutter, Riverpod, GoRouter
- **Infrastructure**: Docker, Docker Compose
- **Architecture**: Event-driven, Multi-agent orchestration

Happy coding! 🚀
