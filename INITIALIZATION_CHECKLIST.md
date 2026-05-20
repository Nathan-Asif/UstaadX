# UstaadX Initialization Checklist

Use this checklist to verify your setup and start development.

## ✅ Initial Setup

### Prerequisites Installed
- [ ] Docker Desktop installed and running
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Flutter 3.19+ installed (`flutter --version`)
- [ ] Git installed (`git --version`)

### Repository Setup
- [ ] Repository cloned
- [ ] Navigate to project root (`cd ustaadx`)

### Environment Configuration
- [ ] Backend `.env` file created (`apps/backend_api/.env`)
- [ ] Mobile `.env` file created (`apps/mobile_app/.env`)
- [ ] SECRET_KEY updated in backend `.env` (for production)

## ✅ Backend Setup

### Installation
- [ ] Virtual environment created (`python -m venv venv`)
- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)

### Database
- [ ] PostgreSQL running (`docker-compose ps`)
- [ ] Database migrations run (`alembic upgrade head`)
- [ ] Can connect to database (`psql -h localhost -U ustaadx -d ustaadx_db`)

### Redis
- [ ] Redis running (`docker-compose ps`)
- [ ] Can connect to Redis (`redis-cli ping`)

### Backend Server
- [ ] Server starts without errors (`uvicorn app.main:app --reload`)
- [ ] Health endpoint responds (`curl http://localhost:8000/health`)
- [ ] API docs accessible (`http://localhost:8000/docs`)

### Celery
- [ ] Celery worker starts (`celery -A app.core.celery_app worker --loglevel=info`)

## ✅ Mobile Setup

### Installation
- [ ] Flutter dependencies installed (`flutter pub get`)
- [ ] Code generation complete (`flutter pub run build_runner build`)

### Mobile App
- [ ] App builds successfully (`flutter build apk --debug` or similar)
- [ ] App runs on device/emulator (`flutter run`)
- [ ] Home screen displays

## ✅ Code Quality

### Backend
- [ ] Linting passes (`ruff check app/`)
- [ ] Formatting correct (`black --check app/`)
- [ ] Tests run (`pytest`)

### Mobile
- [ ] Analysis passes (`flutter analyze`)
- [ ] Formatting correct (`dart format --set-exit-if-changed lib/`)
- [ ] Tests run (`flutter test`)

## ✅ Docker

### Services Running
- [ ] PostgreSQL container running
- [ ] Redis container running
- [ ] Backend container running (optional)
- [ ] Celery worker container running (optional)

### Docker Commands Work
- [ ] `docker-compose up -d` starts services
- [ ] `docker-compose ps` shows running services
- [ ] `docker-compose logs` shows logs
- [ ] `docker-compose down` stops services

## ✅ Documentation

### Read Key Documents
- [ ] [README.md](README.md) - Project overview
- [ ] [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [ ] [docs/architecture.md](docs/architecture.md) - Architecture overview
- [ ] [docs/setup_guide.md](docs/setup_guide.md) - Detailed setup
- [ ] [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines

### Understand Core Concepts
- [ ] Event-driven architecture
- [ ] Workflow engine
- [ ] Agent system
- [ ] API conventions

## ✅ Development Environment

### IDE Setup
- [ ] IDE/Editor configured (VS Code recommended)
- [ ] Python extension installed (for VS Code)
- [ ] Flutter extension installed (for VS Code)
- [ ] Docker extension installed (for VS Code)

### Git Configuration
- [ ] Git user configured (`git config user.name` and `user.email`)
- [ ] SSH keys set up (if using SSH)
- [ ] Can create branches
- [ ] Can commit changes

## ✅ First Development Task

### Backend Task
- [ ] Create a simple model in `app/models/`
- [ ] Create corresponding schema in `app/schemas/`
- [ ] Create migration (`alembic revision --autogenerate`)
- [ ] Run migration (`alembic upgrade head`)
- [ ] Create API endpoint in `app/api/v1/routes/`
- [ ] Test endpoint in Swagger UI

### Mobile Task
- [ ] Create a simple widget in `lib/shared/widgets/`
- [ ] Use widget in home page
- [ ] Hot reload works
- [ ] Widget displays correctly

## ✅ Testing

### Backend Testing
- [ ] Can run all tests (`pytest`)
- [ ] Can run specific test (`pytest tests/test_file.py`)
- [ ] Coverage report generated (`pytest --cov=app`)

### Mobile Testing
- [ ] Can run all tests (`flutter test`)
- [ ] Can run specific test (`flutter test test/file_test.dart`)
- [ ] Coverage report generated (`flutter test --coverage`)

## ✅ CI/CD

### GitHub Actions
- [ ] Backend CI workflow exists (`.github/workflows/backend-ci.yml`)
- [ ] Mobile CI workflow exists (`.github/workflows/mobile-ci.yml`)
- [ ] Workflows run on push (after first push)

## ✅ Production Readiness (Before Deployment)

### Security
- [ ] SECRET_KEY changed from default
- [ ] Database password changed from default
- [ ] CORS origins configured for production
- [ ] HTTPS enabled
- [ ] Environment variables secured

### Infrastructure
- [ ] Using managed PostgreSQL (not Docker)
- [ ] Using managed Redis (not Docker)
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Logging aggregation set up

### Performance
- [ ] Load testing completed
- [ ] Database queries optimized
- [ ] Caching strategy implemented
- [ ] Rate limiting configured

## 🎯 Next Steps

Once all checks are complete:

1. **Start Building Features**
   - Define your data models
   - Implement API endpoints
   - Build mobile UI
   - Connect events and workflows

2. **Follow Best Practices**
   - Write tests for new code
   - Follow code style guidelines
   - Document your changes
   - Create meaningful commits

3. **Collaborate**
   - Create feature branches
   - Submit pull requests
   - Review code
   - Share knowledge

## 📞 Getting Help

If you're stuck on any item:

1. Check the relevant documentation
2. Search existing issues
3. Ask in team chat
4. Create a new issue with details

## ✨ You're Ready!

Once this checklist is complete, you have a fully functional development environment and are ready to build UstaadX features!

**Happy coding! 🚀**
