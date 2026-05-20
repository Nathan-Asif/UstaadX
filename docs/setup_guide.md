# UstaadX Setup Guide

## Prerequisites

### Required Software

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Python** 3.11+
- **Flutter** 3.19+
- **PostgreSQL** 15+ (or use Docker)
- **Redis** 7+ (or use Docker)
- **Git**

### Recommended Tools

- **VS Code** with extensions:
  - Python
  - Flutter
  - Docker
  - GitLens
- **Postman** or **Insomnia** for API testing
- **pgAdmin** or **DBeaver** for database management

## Initial Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd ustaadx
```

### 2. Environment Configuration

#### Backend Environment

```bash
cd apps/backend_api
cp .env.example .env
```

Edit `.env` and update values:
- `SECRET_KEY`: Generate a secure random key
- `DATABASE_URL`: Update if not using Docker
- `REDIS_URL`: Update if not using Docker

#### Mobile Environment

```bash
cd apps/mobile_app
cp .env.example .env
```

Edit `.env` and update:
- `API_BASE_URL`: Your backend URL
- `WS_BASE_URL`: Your WebSocket URL

### 3. Docker Setup (Recommended)

Start all services with Docker Compose:

```bash
# From project root
docker-compose up -d
```

This starts:
- PostgreSQL on port 5432
- Redis on port 6379
- Backend API on port 8000
- Celery worker

Check services:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs -f backend
```

### 4. Backend Setup (Local Development)

#### Create Virtual Environment

```bash
cd apps/backend_api
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Database Migration

```bash
# Initialize Alembic (first time only)
alembic revision --autogenerate -m "Initial migration"

# Run migrations
alembic upgrade head
```

#### Run Backend

```bash
# Development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Run Celery Worker

In a separate terminal:

```bash
cd apps/backend_api
source venv/bin/activate  # or venv\Scripts\activate on Windows
celery -A app.core.celery_app worker --loglevel=info
```

### 5. Mobile App Setup

#### Install Flutter Dependencies

```bash
cd apps/mobile_app
flutter pub get
```

#### Generate Code

```bash
# Generate Riverpod and Freezed code
flutter pub run build_runner build --delete-conflicting-outputs
```

#### Run Mobile App

```bash
# List available devices
flutter devices

# Run on specific device
flutter run -d <device-id>

# Or just run (will prompt for device)
flutter run
```

## Verification

### Backend Health Check

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

### API Documentation

Open in browser:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Connection

```bash
# Using psql
psql -h localhost -U ustaadx -d ustaadx_db

# Password: ustaadx_dev_password
```

### Redis Connection

```bash
# Using redis-cli
redis-cli -h localhost -p 6379
> ping
PONG
```

## Development Workflow

### Backend Development

1. **Create new migration**:
   ```bash
   alembic revision --autogenerate -m "Description"
   alembic upgrade head
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Code formatting**:
   ```bash
   black app/
   ruff check app/
   ```

4. **Type checking**:
   ```bash
   mypy app/
   ```

### Mobile Development

1. **Generate code after changes**:
   ```bash
   flutter pub run build_runner watch
   ```

2. **Run tests**:
   ```bash
   flutter test
   ```

3. **Analyze code**:
   ```bash
   flutter analyze
   ```

4. **Format code**:
   ```bash
   flutter format lib/
   ```

## Common Issues

### Issue: Port Already in Use

**Solution**:
```bash
# Find process using port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Kill process or change port in .env
```

### Issue: Database Connection Failed

**Solution**:
- Check PostgreSQL is running: `docker-compose ps`
- Verify DATABASE_URL in .env
- Check PostgreSQL logs: `docker-compose logs postgres`

### Issue: Redis Connection Failed

**Solution**:
- Check Redis is running: `docker-compose ps`
- Verify REDIS_URL in .env
- Check Redis logs: `docker-compose logs redis`

### Issue: Flutter Build Runner Conflicts

**Solution**:
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### Issue: Alembic Migration Conflicts

**Solution**:
```bash
# Reset to specific revision
alembic downgrade <revision>

# Or reset completely
alembic downgrade base
alembic upgrade head
```

## Environment-Specific Setup

### Development
- Use Docker Compose for services
- Enable debug logging
- Use hot reload

### Staging
- Use environment-specific .env
- Disable debug mode
- Enable error tracking

### Production
- Use managed database (AWS RDS, etc.)
- Use managed Redis (ElastiCache, etc.)
- Enable all security features
- Use production SECRET_KEY
- Enable HTTPS only
- Configure proper CORS origins

## Next Steps

1. Read [Architecture Documentation](architecture.md)
2. Review [API Conventions](api_conventions.md)
3. Understand [Event System](event_system.md)
4. Explore [Workflow Engine](workflow_engine.md)
5. Start building features!

## Useful Commands

### Docker

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build

# View logs
docker-compose logs -f [service-name]

# Execute command in container
docker-compose exec backend bash
```

### Database

```bash
# Create backup
docker-compose exec postgres pg_dump -U ustaadx ustaadx_db > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U ustaadx ustaadx_db < backup.sql

# Reset database
docker-compose down -v
docker-compose up -d
```

### Git

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Commit with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update documentation"

# Push and create PR
git push origin feature/your-feature-name
```

## Support

For issues or questions:
1. Check this documentation
2. Review architecture docs
3. Check existing issues
4. Create new issue with details
