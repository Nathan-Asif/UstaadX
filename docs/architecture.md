# UstaadX Architecture

## Overview

UstaadX is an **event-driven multi-agent orchestration platform** designed to coordinate service providers, customers, and automated workflows in Pakistan's informal service economy.

## Core Architectural Principles

### 1. Event-Driven Architecture
- All state changes emit events
- Loose coupling between components
- Asynchronous processing
- Event sourcing ready

### 2. Multi-Agent System
- Specialized agents for different tasks
- Agent coordination through workflows
- Pluggable agent architecture
- Future AI/ML integration ready

### 3. Real-time Communication
- WebSocket support for live updates
- Push notifications
- Bidirectional communication
- Connection management

### 4. Clean Architecture
- Separation of concerns
- Dependency inversion
- Testability
- Maintainability

## System Components

### Backend (FastAPI)

```
┌─────────────────────────────────────────────────┐
│                  API Layer                       │
│  (FastAPI Routes, WebSocket Endpoints)          │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Service Layer                       │
│  (Business Logic, Orchestration)                │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Event Bus & Workflows                   │
│  (Event Distribution, Workflow Engine)          │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              Agent System                        │
│  (Matcher, Negotiator, Scheduler, etc.)        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Repository Layer                        │
│  (Data Access, ORM)                             │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│            Database Layer                        │
│  (PostgreSQL, Redis)                            │
└─────────────────────────────────────────────────┘
```

### Mobile App (Flutter)

```
┌─────────────────────────────────────────────────┐
│           Presentation Layer                     │
│  (Pages, Widgets, UI Components)                │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          State Management                        │
│  (Riverpod Providers, State)                    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│            Domain Layer                          │
│  (Business Logic, Use Cases)                    │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│             Data Layer                           │
│  (Repositories, API Client, WebSocket)          │
└─────────────────────────────────────────────────┘
```

## Event Flow

```
User Action
    │
    ▼
API Endpoint
    │
    ▼
Service Layer ──► Emit Event
    │                 │
    ▼                 ▼
Database         Event Bus
                      │
                      ▼
              ┌───────┴───────┐
              │               │
              ▼               ▼
         Workflow         Agent System
         Engine           (Process Event)
              │               │
              └───────┬───────┘
                      │
                      ▼
              Emit New Events
                      │
                      ▼
              WebSocket Push
                      │
                      ▼
              Mobile App Update
```

## Agent System

### Agent Types

1. **Matcher Agent**: Matches customers with service providers
2. **Negotiator Agent**: Handles price and terms negotiation
3. **Scheduler Agent**: Manages appointment scheduling
4. **Follow-up Agent**: Automated follow-ups and reminders
5. **Quality Checker Agent**: Quality assurance and feedback
6. **Coordinator Agent**: Orchestrates multiple agents

### Agent Communication

Agents communicate through:
- Event subscriptions
- Workflow steps
- Direct invocation
- Message passing

## Workflow Engine

### Workflow Lifecycle

1. **Pending**: Workflow created, not started
2. **Running**: Workflow executing steps
3. **Paused**: Workflow paused (waiting for external input)
4. **Completed**: All steps completed successfully
5. **Failed**: Workflow failed at some step
6. **Cancelled**: Workflow cancelled by user/system

### Example Workflow: Service Booking

```
1. Booking Created Event
   ↓
2. Matcher Agent: Find suitable providers
   ↓
3. Emit Provider Matched Event
   ↓
4. Negotiator Agent: Handle price negotiation
   ↓
5. Emit Negotiation Accepted Event
   ↓
6. Scheduler Agent: Schedule appointment
   ↓
7. Emit Provider Confirmed Event
   ↓
8. Follow-up Agent: Send reminders
   ↓
9. Workflow Completed
```

## Data Flow

### Request Flow
```
Mobile App → API Gateway → Service → Repository → Database
```

### Response Flow
```
Database → Repository → Service → API Response → Mobile App
```

### Real-time Flow
```
Event → Event Bus → WebSocket Manager → Mobile App
```

## Technology Decisions

### Backend: FastAPI
- **Why**: Async support, fast, modern Python, auto-documentation
- **Alternatives considered**: Django, Flask

### Database: PostgreSQL
- **Why**: ACID compliance, JSON support, mature, scalable
- **Alternatives considered**: MySQL, MongoDB

### Cache: Redis
- **Why**: Fast, pub/sub support, versatile data structures
- **Alternatives considered**: Memcached

### Task Queue: Celery
- **Why**: Mature, distributed, Python native
- **Alternatives considered**: RQ, Dramatiq

### Mobile: Flutter
- **Why**: Cross-platform, fast, single codebase
- **Alternatives considered**: React Native, Native

### State Management: Riverpod
- **Why**: Type-safe, compile-time safety, testable
- **Alternatives considered**: Bloc, Provider

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Load balancer ready
- Database connection pooling
- Redis for shared state

### Vertical Scaling
- Async I/O throughout
- Database query optimization
- Caching strategy
- Background job processing

### Future Enhancements
- Microservices migration path
- Message queue (RabbitMQ/Kafka)
- Service mesh
- Kubernetes deployment

## Security Architecture

### Authentication
- JWT tokens
- Refresh token rotation
- Secure storage (mobile)

### Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- API rate limiting

### Data Protection
- Encryption at rest
- Encryption in transit (TLS)
- Secure environment variables
- Secret management

## Monitoring & Observability

### Logging
- Structured logging (JSON)
- Log levels
- Request/response logging
- Error tracking

### Metrics (Future)
- API response times
- Database query performance
- Event processing latency
- Agent execution metrics

### Tracing (Future)
- Distributed tracing
- Correlation IDs
- Event flow tracking
- Workflow visualization

## Development Workflow

1. Feature branch from `develop`
2. Implement with tests
3. Code review
4. Merge to `develop`
5. Deploy to staging
6. Test
7. Merge to `main`
8. Deploy to production
