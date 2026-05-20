# Event System Documentation

## Overview

UstaadX uses an **event-driven architecture** where all significant state changes emit events. This enables loose coupling, asynchronous processing, and complex workflow orchestration.

## Core Concepts

### Events

Events are immutable records of something that happened in the system. They contain:
- **event_id**: Unique identifier
- **event_type**: Type of event (enum)
- **timestamp**: When it occurred
- **source**: Component that emitted it
- **correlation_id**: For tracing related events
- **payload**: Event-specific data
- **metadata**: Additional context

### Event Bus

The Event Bus is the central hub for event distribution. It:
- Receives published events
- Routes events to subscribers
- Handles errors gracefully
- Logs all event activity

### Event Handlers

Event handlers are functions that react to specific event types. They:
- Subscribe to event types
- Process events asynchronously
- Can emit new events
- Should be idempotent

## Event Types

### Booking Events

```python
BOOKING_CREATED       # New booking created
BOOKING_UPDATED       # Booking details changed
BOOKING_CANCELLED     # Booking cancelled
BOOKING_COMPLETED     # Service completed
```

### Provider Events

```python
PROVIDER_MATCHED      # Provider matched to booking
PROVIDER_CONFIRMED    # Provider accepted booking
PROVIDER_REJECTED     # Provider declined booking
PROVIDER_ARRIVED      # Provider arrived at location
```

### Negotiation Events

```python
NEGOTIATION_STARTED   # Price negotiation started
NEGOTIATION_OFFER_MADE # New offer made
NEGOTIATION_ACCEPTED  # Offer accepted
NEGOTIATION_REJECTED  # Offer rejected
```

### Workflow Events

```python
WORKFLOW_STARTED      # Workflow execution started
WORKFLOW_STEP_COMPLETED # Step completed
WORKFLOW_COMPLETED    # Workflow finished
WORKFLOW_FAILED       # Workflow failed
```

### Agent Events

```python
AGENT_TASK_ASSIGNED   # Task assigned to agent
AGENT_TASK_COMPLETED  # Agent completed task
AGENT_TASK_FAILED     # Agent task failed
```

## Event Structure

### Base Event

```python
{
  "event_id": "uuid",
  "event_type": "booking.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "source": "booking_service",
  "correlation_id": "uuid",
  "payload": {
    "booking_id": "123",
    "customer_id": "456",
    "service_type": "plumber"
  },
  "metadata": {
    "user_agent": "mobile_app",
    "ip_address": "192.168.1.1"
  }
}
```

## Publishing Events

### From Service Layer

```python
from app.events import event_bus, BaseEvent, EventType

async def create_booking(booking_data):
    # Create booking in database
    booking = await booking_repository.create(booking_data)
    
    # Emit event
    event = BaseEvent(
        event_type=EventType.BOOKING_CREATED,
        source="booking_service",
        payload={
            "booking_id": str(booking.id),
            "customer_id": str(booking.customer_id),
            "service_type": booking.service_type,
        }
    )
    
    await event_bus.publish(event)
    
    return booking
```

## Subscribing to Events

### Register Event Handler

```python
from app.events import event_bus, EventType, BaseEvent

async def handle_booking_created(event: BaseEvent):
    """Handle booking created event"""
    booking_id = event.payload["booking_id"]
    
    # Trigger matcher agent
    await matcher_agent.find_providers(booking_id)
    
    # Emit new event
    await event_bus.publish(BaseEvent(
        event_type=EventType.AGENT_TASK_ASSIGNED,
        source="event_handler",
        payload={"agent": "matcher", "booking_id": booking_id}
    ))

# Subscribe handler to event type
event_bus.subscribe(EventType.BOOKING_CREATED, handle_booking_created)
```

## Event Flow Examples

### Example 1: Booking Creation Flow

```
1. User creates booking
   ↓
2. API creates booking in DB
   ↓
3. Emit BOOKING_CREATED event
   ↓
4. Matcher agent handler triggered
   ↓
5. Matcher finds providers
   ↓
6. Emit PROVIDER_MATCHED event
   ↓
7. Notification handler triggered
   ↓
8. Send notifications to providers
   ↓
9. WebSocket push to mobile app
```

### Example 2: Provider Confirmation Flow

```
1. Provider accepts booking
   ↓
2. API updates booking status
   ↓
3. Emit PROVIDER_CONFIRMED event
   ↓
4. Scheduler agent handler triggered
   ↓
5. Create calendar entry
   ↓
6. Emit WORKFLOW_STEP_COMPLETED event
   ↓
7. Follow-up agent handler triggered
   ↓
8. Schedule reminder tasks
   ↓
9. Emit FOLLOWUP_TRIGGERED event
```

## Event Patterns

### 1. Command Events
Events that trigger actions:
```python
BOOKING_CREATED → Trigger matching workflow
PROVIDER_MATCHED → Send notifications
```

### 2. State Change Events
Events that record state transitions:
```python
BOOKING_UPDATED → Record audit log
WORKFLOW_COMPLETED → Update dashboard
```

### 3. Integration Events
Events for external systems:
```python
BOOKING_COMPLETED → Trigger payment
PROVIDER_CONFIRMED → Update calendar
```

## Best Practices

### Event Design

1. **Events are immutable**: Never modify an event after creation
2. **Events are facts**: Name events in past tense (CREATED, not CREATE)
3. **Include context**: Add enough data for handlers to act
4. **Keep payload focused**: Only include relevant data
5. **Use correlation IDs**: Track related events

### Event Handlers

1. **Idempotent**: Handle duplicate events gracefully
2. **Fast**: Don't block event processing
3. **Resilient**: Handle errors without crashing
4. **Focused**: One handler, one responsibility
5. **Async**: Use async/await for I/O operations

### Error Handling

```python
async def handle_event(event: BaseEvent):
    try:
        # Process event
        await process_event(event)
    except Exception as e:
        # Log error
        logger.error("Event processing failed", 
                    event_id=event.event_id, 
                    error=str(e))
        
        # Emit error event
        await event_bus.publish(BaseEvent(
            event_type=EventType.SYSTEM_ERROR,
            source="event_handler",
            payload={
                "original_event_id": str(event.event_id),
                "error": str(e)
            }
        ))
```

## Testing Events

### Unit Testing Event Handlers

```python
import pytest
from app.events import BaseEvent, EventType

@pytest.mark.asyncio
async def test_booking_created_handler():
    # Arrange
    event = BaseEvent(
        event_type=EventType.BOOKING_CREATED,
        source="test",
        payload={"booking_id": "123"}
    )
    
    # Act
    await handle_booking_created(event)
    
    # Assert
    # Verify expected side effects
```

### Integration Testing Event Flow

```python
@pytest.mark.asyncio
async def test_booking_creation_flow():
    # Create booking
    booking = await create_booking(booking_data)
    
    # Wait for async processing
    await asyncio.sleep(0.1)
    
    # Verify events were emitted
    assert event_was_published(EventType.BOOKING_CREATED)
    assert event_was_published(EventType.AGENT_TASK_ASSIGNED)
```

## Monitoring Events

### Event Metrics (Future)

- Events published per type
- Event processing latency
- Failed event handlers
- Event throughput

### Event Logging

All events are logged with structured logging:

```json
{
  "level": "info",
  "message": "event_published",
  "event_id": "uuid",
  "event_type": "booking.created",
  "source": "booking_service",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Future Enhancements

### Event Store
- Persist all events for audit trail
- Enable event replay
- Support event sourcing

### Message Queue
- Replace in-memory bus with Redis Pub/Sub
- Add RabbitMQ or Kafka for durability
- Enable distributed event processing

### Event Versioning
- Support multiple event versions
- Handle schema evolution
- Backward compatibility

### Dead Letter Queue
- Capture failed events
- Retry mechanism
- Manual intervention support

## Related Documentation

- [Architecture Overview](architecture.md)
- [Workflow Engine](workflow_engine.md)
- [API Conventions](api_conventions.md)
