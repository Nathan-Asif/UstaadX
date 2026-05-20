# UstaadX

**AI-Powered Operational Orchestration for Pakistan's Informal Service Economy**

[![Backend CI](https://github.com/your-org/ustaadx/workflows/Backend%20CI/badge.svg)](https://github.com/your-org/ustaadx/actions)
[![Mobile CI](https://github.com/your-org/ustaadx/workflows/Mobile%20CI/badge.svg)](https://github.com/your-org/ustaadx/actions)

> **👉 New here? Start with [START_HERE.md](START_HERE.md) for a guided introduction!**

UstaadX is an **event-driven multi-agent orchestration platform** designed to coordinate service providers, customers, and automated workflows in Pakistan's informal service economy.

> **⚠️ Hackathon MVP**: This is a production-grade foundation built for rapid feature development. The architecture is ready for scale, but business features are yet to be implemented.
>
> **📊 Foundation Stats**: 43 directories, 74 files, complete event-driven architecture with multi-agent orchestration

## 🚀 Quick Start

**Get started in 5 minutes:**

```bash
# Automated setup (recommended)
./infra/scripts/setup.sh  # Linux/Mac
# or
infra\scripts\setup.bat   # Windows

# Manual setup
docker-compose up -d
cd apps/backend_api && pip install -r requirements.txt
cd apps/mobile_app && flutter pub get
```

📖 **[Read the Quick Start Guide](QUICKSTART.md)** for detailed instructions.

## 🏗️ Architecture

### Core Principles

1. **Event-Driven Architecture** - All state changes emit events for loose coupling
2. **Multi-Agent Orchestration** - Specialized agents coordinate complex workflows
3. **Real-time Communication** - WebSocket support for live updates
4. **Clean Architecture** - Separation of concerns, testability, maintainability
5. **Scalability First** - Designed for horizontal scaling from day one

### System Overview

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Mobile    │◄────►│  Backend API │◄────►│  Database   │
│     App     │ WS   │   (FastAPI)  │      │ (Postgres)  │
└─────────────┘      └──────┬───────┘      └─────────────┘
                            │
                     ┌──────▼───────┐
                     │  Event Bus   │
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌─────────┐   ┌─────────┐   ┌─────────┐
        │ Matcher │   │Negotiator│   │Scheduler│
        │  Agent  │   │  Agent   │   │  Agent  │
        └─────────┘   └─────────┘   └─────────┘
```

📖 **[Read the Architecture Guide](docs/architecture.md)** for deep dive.

## 📁 Project Structure

```
ustaadx/
├── apps/
│   ├── backend_api/          # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/          # API routes
│   │   │   ├── core/         # Config, logging, security
│   │   │   ├── db/           # Database setup
│   │   │   ├── events/       # Event system
│   │   │   ├── workflows/    # Workflow engine
│   │   │   ├── agents/       # Agent system
│   │   │   ├── websockets/   # WebSocket manager
│   │   │   ├── models/       # Database models
│   │   │   ├── schemas/      # Pydantic schemas
│   │   │   ├── services/     # Business logic
│   │   │   └── repositories/ # Data access
│   │   └── alembic/          # Database migrations
│   └── mobile_app/           # Flutter mobile app
│       └── lib/
│           ├── core/         # Config, network, theme
│           ├── features/     # Feature modules
│           └── shared/       # Shared components
├── packages/
│   └── shared_models/        # Shared data models
├── infra/
│   ├── docker/               # Docker configs
│   └── scripts/              # Setup scripts
├── docs/                     # Documentation
│   ├── architecture.md       # System architecture
│   ├── event_system.md       # Event-driven design
│   ├── workflow_engine.md    # Workflow orchestration
│   ├── api_conventions.md    # API standards
│   └── setup_guide.md        # Detailed setup
└── docker-compose.yml        # Local dev stack
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **PostgreSQL** - Primary database with ACID compliance
- **Redis** - Caching and pub/sub messaging
- **Celery** - Distributed task queue
- **SQLAlchemy** - Async ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Structlog** - Structured logging

### Mobile
- **Flutter** - Cross-platform mobile framework
- **Riverpod** - Type-safe state management
- **GoRouter** - Declarative routing
- **Dio** - HTTP client with interceptors
- **WebSocket** - Real-time communication
- **Freezed** - Immutable data classes

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Local orchestration
- **GitHub Actions** - CI/CD pipelines

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Quick Start](QUICKSTART.md) | Get running in 5 minutes |
| [Setup Guide](docs/setup_guide.md) | Detailed setup instructions |
| [Architecture](docs/architecture.md) | System design and decisions |
| [Event System](docs/event_system.md) | Event-driven architecture |
| [Workflow Engine](docs/workflow_engine.md) | Workflow orchestration |
| [API Conventions](docs/api_conventions.md) | REST API standards |
| [Contributing](CONTRIBUTING.md) | Development guidelines |
| [Foundation Summary](PROJECT_FOUNDATION.md) | What was built |

## 🎯 What's Implemented

### ✅ Complete Foundation
- Event-driven architecture with event bus
- Workflow engine with step orchestration
- Multi-agent system with base abstractions
- WebSocket manager for real-time updates
- Database setup with migrations
- API versioning structure
- Structured logging
- Security utilities (JWT, password hashing)
- Docker development environment
- CI/CD pipelines
- Comprehensive documentation

### 🚧 Ready for Implementation
- Database models (User, Provider, Booking, etc.)
- API endpoints (auth, bookings, providers)
- Business logic services
- Event handlers
- Concrete workflows
- Concrete agents
- Mobile UI screens
- AI/ML integration (Gemini, Antigravity)

## 🚦 Getting Started

### 1. Prerequisites

Install these first:
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Python 3.11+](https://www.python.org/downloads/)
- [Flutter 3.19+](https://flutter.dev/docs/get-started/install)
- [Git](https://git-scm.com/downloads)

### 2. Quick Setup

```bash
# Clone and setup
git clone <repo-url>
cd ustaadx
./infra/scripts/setup.sh  # Automated setup

# Or use Make
make setup
make docker-up
make backend-run  # In one terminal
make mobile-run   # In another terminal
```

### 3. Verify Installation

```bash
# Check backend health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Check database
docker-compose exec postgres psql -U ustaadx -d ustaadx_db
```

## 🧪 Development

### Backend Development

```bash
cd apps/backend_api

# Run server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/

# Lint code
ruff check app/

# Create migration
alembic revision --autogenerate -m "description"
```

### Mobile Development

```bash
cd apps/mobile_app

# Run app
flutter run

# Run tests
flutter test

# Format code
flutter format lib/

# Analyze code
flutter analyze

# Generate code
flutter pub run build_runner build --delete-conflicting-outputs
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow
- Code style guidelines
- Commit conventions
- PR process

## 📊 Project Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend Foundation | ✅ Complete | Event system, workflows, agents ready |
| Mobile Foundation | ✅ Complete | Network, routing, state management ready |
| Database Models | 🚧 Ready | Implement in `app/models/` |
| API Endpoints | 🚧 Ready | Implement in `app/api/v1/routes/` |
| Business Logic | 🚧 Ready | Implement in `app/services/` |
| Event Handlers | 🚧 Ready | Subscribe to events |
| Workflows | 🚧 Ready | Create concrete workflows |
| Agents | 🚧 Ready | Implement agent logic |
| Mobile UI | 🚧 Ready | Build feature screens |
| AI Integration | 📋 Planned | Gemini, Antigravity |

## 🎓 Learning Resources

### Understanding the Architecture
1. Start with [Architecture Overview](docs/architecture.md)
2. Learn about [Event System](docs/event_system.md)
3. Understand [Workflow Engine](docs/workflow_engine.md)
4. Review [API Conventions](docs/api_conventions.md)

### Building Features
1. Define models in `app/models/`
2. Create schemas in `app/schemas/`
3. Implement services in `app/services/`
4. Add API routes in `app/api/v1/routes/`
5. Subscribe to events in event bus
6. Create workflows for complex processes
7. Implement agents for automation

## 🐛 Troubleshooting

Common issues and solutions:

**Port already in use:**
```bash
docker-compose down
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # Mac/Linux
```

**Database connection error:**
```bash
docker-compose restart postgres
docker-compose logs postgres
```

**Flutter build issues:**
```bash
flutter clean
flutter pub get
flutter pub run build_runner build --delete-conflicting-outputs
```

See [Setup Guide](docs/setup_guide.md) for more troubleshooting.

## 📝 License

[License Type] - See LICENSE file

## 🙏 Acknowledgments

Built with production-grade architecture discipline for hackathon velocity.

---

**Ready to build features?** Start with [Quick Start Guide](QUICKSTART.md) 🚀
