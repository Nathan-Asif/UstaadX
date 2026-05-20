# Next Steps - Building UstaadX Features

The foundation is complete. Here's your roadmap for building actual features.

## 🎯 Immediate Next Steps (Week 1)

### 1. Initialize the Project

```bash
# Run the setup script
./infra/scripts/setup.sh  # Linux/Mac
# or
infra\scripts\setup.bat   # Windows

# Verify everything works
curl http://localhost:8000/health
```

### 2. Define Core Data Models

**Backend** (`apps/backend_api/app/models/`)

Create these models first:

```python
# user.py
class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    user_type = Column(Enum(UserType), nullable=False)  # CUSTOMER, PROVIDER
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String, nullable=False)

# provider.py
class Provider(Base, TimestampMixin):
    __tablename__ = "providers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    service_type = Column(String, nullable=False)  # plumber, electrician, etc.
    rating = Column(Float, default=0.0)
    total_jobs = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    location = Column(JSON)  # {lat, lng, address}

# booking.py
class Booking(Base, TimestampMixin):
    __tablename__ = "bookings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=True)
    service_type = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    location = Column(JSON)
    preferred_date = Column(Date)
    preferred_time = Column(Time)
    final_price = Column(Numeric(10, 2), nullable=True)
```

**Create Migration:**
```bash
cd apps/backend_api
alembic revision --autogenerate -m "Add user, provider, booking models"
alembic upgrade head
```

### 3. Create Pydantic Schemas

**Backend** (`apps/backend_api/app/schemas/`)

```python
# user.py
class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    full_name: str
    password: str
    user_type: UserType

class UserResponse(BaseModel):
    id: UUID
    email: str
    phone: str
    full_name: str
    user_type: UserType
    created_at: datetime

# booking.py
class BookingCreate(BaseModel):
    service_type: str
    description: str
    location: dict
    preferred_date: date
    preferred_time: time

class BookingResponse(BaseModel):
    id: UUID
    customer_id: UUID
    service_type: str
    status: BookingStatus
    created_at: datetime
```

### 4. Implement Authentication

**Backend** (`apps/backend_api/app/api/v1/routes/auth.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, service: AuthService = Depends()):
    return await service.register(user_data)

@router.post("/login", response_model=Token)
async def login(email: str, password: str, service: AuthService = Depends()):
    return await service.login(email, password)

@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user = Depends(get_current_user)):
    return current_user
```

**Service** (`apps/backend_api/app/services/auth_service.py`)

```python
class AuthService:
    async def register(self, user_data: UserCreate) -> User:
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = await user_repository.create({
            **user_data.dict(exclude={"password"}),
            "hashed_password": hashed_password
        })
        
        # Emit event
        await event_bus.publish(BaseEvent(
            event_type=EventType.USER_REGISTERED,
            source="auth_service",
            payload={"user_id": str(user.id)}
        ))
        
        return user
    
    async def login(self, email: str, password: str) -> Token:
        # Verify credentials
        user = await user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create token
        access_token = create_access_token({"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")
```

### 5. Implement Booking Flow

**API Endpoint** (`apps/backend_api/app/api/v1/routes/bookings.py`)

```python
@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    current_user = Depends(get_current_user),
    service: BookingService = Depends()
):
    return await service.create_booking(booking_data, current_user.id)
```

**Service** (`apps/backend_api/app/services/booking_service.py`)

```python
class BookingService:
    async def create_booking(self, booking_data: BookingCreate, customer_id: UUID):
        # Create booking
        booking = await booking_repository.create({
            **booking_data.dict(),
            "customer_id": customer_id,
            "status": BookingStatus.PENDING
        })
        
        # Emit event to trigger workflow
        await event_bus.publish(BaseEvent(
            event_type=EventType.BOOKING_CREATED,
            source="booking_service",
            payload={
                "booking_id": str(booking.id),
                "customer_id": str(customer_id),
                "service_type": booking.service_type
            }
        ))
        
        return booking
```

### 6. Create Booking Workflow

**Workflow** (`apps/backend_api/app/workflows/booking_workflow.py`)

```python
class BookingWorkflow(Workflow):
    def __init__(self):
        super().__init__("booking_workflow")
        self.add_step(FindProvidersStep())
        self.add_step(NotifyProvidersStep())
        self.add_step(WaitForConfirmationStep())
        self.add_step(ScheduleAppointmentStep())

# Subscribe to event
async def handle_booking_created(event: BaseEvent):
    workflow = BookingWorkflow()
    context = WorkflowContext(
        correlation_id=event.correlation_id,
        data=event.payload
    )
    await workflow.execute(context)

event_bus.subscribe(EventType.BOOKING_CREATED, handle_booking_created)
```

### 7. Implement Matcher Agent

**Agent** (`apps/backend_api/app/agents/matcher_agent.py`)

```python
class MatcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(AgentType.MATCHER, "provider_matcher")
    
    async def process(self, task: AgentTask) -> AgentResponse:
        booking_id = task.input_data["booking_id"]
        service_type = task.input_data["service_type"]
        location = task.input_data["location"]
        
        # Find matching providers
        providers = await self._find_providers(service_type, location)
        
        # Rank providers
        ranked_providers = await self._rank_providers(providers)
        
        return AgentResponse(
            task_id=task.task_id,
            success=True,
            output_data={
                "providers": [str(p.id) for p in ranked_providers[:5]],
                "count": len(ranked_providers)
            }
        )
    
    async def _find_providers(self, service_type: str, location: dict):
        # Query database for providers
        # Filter by service type, location, availability, rating
        pass
    
    async def _rank_providers(self, providers):
        # Rank by rating, distance, availability
        # Future: Use ML model for intelligent matching
        pass
```

## 🎯 Short-term Goals (Week 2-3)

### Mobile App Development

1. **Authentication Screens**
   ```dart
   // lib/features/auth/presentation/pages/login_page.dart
   // lib/features/auth/presentation/pages/register_page.dart
   ```

2. **Booking Creation Flow**
   ```dart
   // lib/features/booking/presentation/pages/create_booking_page.dart
   // lib/features/booking/presentation/pages/booking_details_page.dart
   ```

3. **Provider Listing**
   ```dart
   // lib/features/provider/presentation/pages/provider_list_page.dart
   // lib/features/provider/presentation/pages/provider_profile_page.dart
   ```

4. **Real-time Updates**
   ```dart
   // Connect WebSocket
   // Listen for booking status updates
   // Show notifications
   ```

### Additional Backend Features

1. **Provider Management**
   - Provider registration
   - Profile management
   - Availability management

2. **Negotiation System**
   - Price negotiation flow
   - Counter-offers
   - Acceptance/rejection

3. **Notifications**
   - Push notifications
   - SMS notifications
   - Email notifications

4. **Reviews & Ratings**
   - Customer reviews
   - Provider ratings
   - Feedback system

## 🎯 Medium-term Goals (Week 4-6)

### AI Integration

1. **Gemini Integration**
   ```python
   # app/services/ai_service.py
   class AIService:
       async def analyze_booking_description(self, description: str):
           # Use Gemini to extract service details
           # Categorize service type
           # Suggest pricing
           pass
   ```

2. **Intelligent Matching**
   - ML-based provider matching
   - Predictive availability
   - Dynamic pricing suggestions

3. **Chatbot**
   - Customer support bot
   - Booking assistance
   - FAQ handling

### Advanced Features

1. **Payment Integration**
   - Payment gateway integration
   - Escrow system
   - Refund handling

2. **Scheduling System**
   - Calendar integration
   - Availability management
   - Reminder system

3. **Analytics Dashboard**
   - Booking metrics
   - Provider performance
   - Revenue tracking

## 🎯 Long-term Goals (Week 7+)

### Scalability

1. **Performance Optimization**
   - Database query optimization
   - Caching strategy
   - CDN for static assets

2. **Monitoring & Observability**
   - Error tracking (Sentry)
   - Performance monitoring (New Relic)
   - Log aggregation (ELK stack)

3. **Infrastructure**
   - Kubernetes deployment
   - Auto-scaling
   - Load balancing

### Advanced AI Features

1. **Google Antigravity Integration**
   - Advanced orchestration
   - Multi-agent coordination
   - Complex workflow automation

2. **Predictive Analytics**
   - Demand forecasting
   - Provider churn prediction
   - Price optimization

3. **Natural Language Processing**
   - Voice booking
   - Multilingual support (Urdu, English)
   - Sentiment analysis

## 📋 Development Checklist

Use this for each feature:

- [ ] Define data models
- [ ] Create database migration
- [ ] Write Pydantic schemas
- [ ] Implement repository layer
- [ ] Implement service layer
- [ ] Create API endpoints
- [ ] Write tests
- [ ] Add event handlers
- [ ] Create workflows (if needed)
- [ ] Implement agents (if needed)
- [ ] Build mobile UI
- [ ] Test end-to-end
- [ ] Document API
- [ ] Update documentation

## 🛠️ Development Tips

1. **Start Small**: Implement one complete feature end-to-end before moving to the next
2. **Test Early**: Write tests as you build, not after
3. **Use Events**: Emit events for all significant state changes
4. **Think Workflows**: Complex processes should be workflows
5. **Agent for Automation**: Use agents for automated decision-making
6. **Document**: Update docs as you build
7. **Review Code**: Get feedback early and often

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flutter Documentation](https://flutter.dev/docs)
- [Riverpod Documentation](https://riverpod.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

## 🚀 Ready to Build!

You have:
- ✅ Complete foundation
- ✅ Clear roadmap
- ✅ Example implementations
- ✅ Best practices

**Now go build something amazing! 🎉**
