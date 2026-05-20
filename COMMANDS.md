# UstaadX Command Reference

Quick reference for all common commands.

## 🚀 Setup Commands

### Initial Setup

```bash
# Automated setup (recommended)
./infra/scripts/setup.sh          # Linux/Mac
infra\scripts\setup.bat            # Windows

# Using Make
make setup                         # Complete setup
make backend-setup                 # Backend only
make mobile-setup                  # Mobile only
```

### Manual Setup

```bash
# Backend
cd apps/backend_api
cp .env.example .env
python -m venv venv
source venv/bin/activate           # Linux/Mac
venv\Scripts\activate              # Windows
pip install -r requirements.txt

# Mobile
cd apps/mobile_app
cp .env.example .env
flutter pub get
```

## 🐳 Docker Commands

### Basic Operations

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart backend

# View logs
docker-compose logs -f
docker-compose logs -f backend     # Specific service

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec postgres psql -U ustaadx -d ustaadx_db
docker-compose exec redis redis-cli
```

### Rebuild Services

```bash
# Rebuild all services
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

## 🐍 Backend Commands

### Development Server

```bash
cd apps/backend_api
source venv/bin/activate           # Linux/Mac
venv\Scripts\activate              # Windows

# Run development server
uvicorn app.main:app --reload

# Run on specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run Celery worker
celery -A app.core.celery_app worker --loglevel=info

# Run Celery beat (scheduler)
celery -A app.core.celery_app beat --loglevel=info
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Show current revision
alembic current

# Show migration history
alembic history

# Reset database (careful!)
alembic downgrade base
alembic upgrade head
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_events.py

# Run specific test
pytest tests/test_events.py::test_event_publishing

# Run with coverage
pytest --cov=app

# Run with coverage report
pytest --cov=app --cov-report=html
pytest --cov=app --cov-report=term-missing

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### Code Quality

```bash
# Format code
black app/
black app/ --check                 # Check only, don't modify

# Lint code
ruff check app/
ruff check app/ --fix              # Auto-fix issues

# Type checking
mypy app/

# Run all quality checks
black app/ && ruff check app/ && mypy app/
```

### Database Operations

```bash
# Connect to database
psql -h localhost -U ustaadx -d ustaadx_db

# Backup database
pg_dump -h localhost -U ustaadx ustaadx_db > backup.sql

# Restore database
psql -h localhost -U ustaadx ustaadx_db < backup.sql

# Using Docker
docker-compose exec postgres pg_dump -U ustaadx ustaadx_db > backup.sql
docker-compose exec -T postgres psql -U ustaadx ustaadx_db < backup.sql
```

### Redis Operations

```bash
# Connect to Redis
redis-cli -h localhost -p 6379

# Using Docker
docker-compose exec redis redis-cli

# Common Redis commands
PING                               # Test connection
KEYS *                             # List all keys
GET key                            # Get value
SET key value                      # Set value
DEL key                            # Delete key
FLUSHALL                           # Clear all data (careful!)
```

## 📱 Mobile Commands

### Development

```bash
cd apps/mobile_app

# Get dependencies
flutter pub get

# Run app
flutter run

# Run on specific device
flutter devices                    # List devices
flutter run -d <device-id>

# Run with specific flavor
flutter run --flavor development
flutter run --flavor production

# Hot reload (in running app)
# Press 'r' in terminal

# Hot restart (in running app)
# Press 'R' in terminal
```

### Code Generation

```bash
# Generate code once
flutter pub run build_runner build

# Generate and delete conflicting outputs
flutter pub run build_runner build --delete-conflicting-outputs

# Watch for changes and regenerate
flutter pub run build_runner watch

# Clean generated files
flutter pub run build_runner clean
```

### Testing

```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/features/auth_test.dart

# Run with coverage
flutter test --coverage

# View coverage report
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html      # Mac
start coverage/html/index.html     # Windows
```

### Code Quality

```bash
# Analyze code
flutter analyze

# Format code
flutter format lib/
flutter format lib/ --set-exit-if-changed  # Check only

# Check for outdated packages
flutter pub outdated
```

### Build

```bash
# Build APK (Android)
flutter build apk
flutter build apk --release
flutter build apk --debug

# Build App Bundle (Android)
flutter build appbundle

# Build iOS
flutter build ios
flutter build ios --release

# Clean build
flutter clean
flutter pub get
```

## 🔧 Utility Commands

### Project Management

```bash
# Using Make
make help                          # Show all commands
make setup                         # Complete setup
make docker-up                     # Start Docker
make docker-down                   # Stop Docker
make backend-run                   # Run backend
make backend-test                  # Test backend
make mobile-run                    # Run mobile
make mobile-test                   # Test mobile
make format                        # Format all code
make lint                          # Lint all code
make clean                         # Clean artifacts
```

### Git Operations

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Commit with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update documentation"
git commit -m "refactor: improve code structure"
git commit -m "test: add tests"

# Push branch
git push origin feature/your-feature-name

# Update from main
git checkout main
git pull origin main
git checkout feature/your-feature-name
git rebase main
```

### Environment Management

```bash
# Backend - Create/activate virtual environment
python -m venv venv
source venv/bin/activate           # Linux/Mac
venv\Scripts\activate              # Windows
deactivate                         # Deactivate

# Backend - Install/update dependencies
pip install -r requirements.txt
pip install <package>
pip freeze > requirements.txt

# Mobile - Update dependencies
flutter pub get
flutter pub upgrade
flutter pub add <package>
```

## 🔍 Debugging Commands

### Backend Debugging

```bash
# Run with debugger
python -m pdb app/main.py

# Check Python version
python --version

# Check installed packages
pip list
pip show <package>

# Check environment variables
printenv | grep DATABASE_URL       # Linux/Mac
set | findstr DATABASE_URL         # Windows
```

### Mobile Debugging

```bash
# Check Flutter installation
flutter doctor
flutter doctor -v

# Check connected devices
flutter devices

# Clear Flutter cache
flutter clean
flutter pub cache repair

# Check app logs
flutter logs

# Run with verbose logging
flutter run -v
```

### Network Debugging

```bash
# Check if port is in use
lsof -i :8000                      # Linux/Mac
netstat -ano | findstr :8000       # Windows

# Kill process on port
kill -9 $(lsof -ti:8000)           # Linux/Mac
taskkill /PID <PID> /F             # Windows

# Test API endpoint
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Test WebSocket
wscat -c ws://localhost:8000/ws/user123
```

## 📊 Monitoring Commands

### Check Service Health

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
docker-compose exec postgres pg_isready -U ustaadx

# Redis connection
docker-compose exec redis redis-cli ping

# Check all services
docker-compose ps
```

### View Logs

```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f postgres

# Redis logs
docker-compose logs -f redis

# Celery logs
docker-compose logs -f celery_worker

# All logs
docker-compose logs -f
```

## 🚨 Emergency Commands

### Reset Everything

```bash
# Stop all services
docker-compose down -v

# Clean Docker
docker system prune -a

# Reset backend
cd apps/backend_api
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic downgrade base
alembic upgrade head

# Reset mobile
cd apps/mobile_app
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

### Fix Common Issues

```bash
# Port already in use
lsof -ti:8000 | xargs kill -9      # Linux/Mac
netstat -ano | findstr :8000       # Windows (then taskkill)

# Database connection issues
docker-compose restart postgres
docker-compose logs postgres

# Redis connection issues
docker-compose restart redis
docker-compose logs redis

# Flutter build issues
flutter clean
rm -rf .dart_tool
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

## 📝 Notes

- Always activate virtual environment before running Python commands
- Use `--help` flag with any command for more options
- Check logs when something doesn't work
- Keep dependencies up to date
- Run tests before committing

## 🔗 Quick Links

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

**Tip**: Bookmark this page for quick reference! 📌
