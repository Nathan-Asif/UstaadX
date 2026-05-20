# Workflow Engine Documentation

## Overview

The Workflow Engine orchestrates complex multi-step processes in UstaadX. It coordinates agents, manages state, handles errors, and ensures reliable execution of business workflows.

## Core Concepts

### Workflow

A workflow is a series of steps executed in sequence to accomplish a business goal. Each workflow:
- Has a unique ID
- Maintains execution state
- Carries context data
- Can be paused and resumed
- Handles errors gracefully

### Workflow Step

A step is a single unit of work within a workflow. Steps:
- Execute independently
- Receive workflow context
- Return updated context
- Can succeed or fail
- Have lifecycle hooks

### Workflow Context

Context is data passed through workflow execution:
- **workflow_id**: Unique identifier
- **state**: Current execution state
- **data**: Business data
- **metadata**: Execution metadata
- **error**: Error information (if failed)

## Workflow States

```python
PENDING    # Created, not started
RUNNING    # Currently executing
PAUSED     # Paused, waiting for input
COMPLETED  # Successfully finished
FAILED     # Execution failed
CANCELLED  # Manually cancelled
```

## Step States

```python
PENDING    # Not yet executed
RUNNING    # Currently executing
COMPLETED  # Successfully finished
FAILED     # Execution failed
SKIPPED    # Skipped (conditional)
```

## Creating Workflows

### Define Workflow Steps

```python
from app.workflows import WorkflowStep, WorkflowContext

class FindProvidersStep(WorkflowStep):
    def __init__(self):
        super().__init__("find_providers")
    
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        booking_id = context.data["booking_id"]
        
        # Find matching providers
        providers = await provider_service.find_matches(booking_id)
        
        # Update context
        context.data["providers"] = providers
        return context
    
    async def on_success(self, context: WorkflowContext):
        # Emit event
        await event_bus.publish(BaseEvent(
            event_type=EventType.PROVIDER_MATCHED,
            source="workflow",
            payload={"booking_id": context.data["booking_id"]}
        ))
    
    async def on_failure(self, context: WorkflowContext, error: Exception):
        # Log error
        logger.error("Provider matching failed", error=str(error))
```

### Compose Workflow

```python
from app.workflows import Workflow

class BookingWorkflow(Workflow):
    def __init__(self):
        super().__init__("booking_workflow")
        
        # Add steps in order
        self.add_step(FindProvidersStep())
        self.add_step(NotifyProvidersStep())
        self.add_step(WaitForConfirmationStep())
        self.add_step(ScheduleAppointmentStep())
        self.add_step(SendRemindersStep())
```

### Execute Workflow

```python
# Create workflow
workflow = BookingWorkflow()

# Create initial context
context = WorkflowContext(
    data={
        "booking_id": "123",
        "customer_id": "456",
        "service_type": "plumber"
    }
)

# Execute
try:
    result = await workflow.execute(context)
    print(f"Workflow completed: {result.workflow_id}")
except Exception as e:
    print(f"Workflow failed: {e}")
```

## Example Workflows

### 1. Booking Creation Workflow

```
Steps:
1. Validate booking data
2. Create booking record
3. Find matching providers
4. Notify providers
5. Wait for confirmation (pause)
6. Schedule appointment
7. Send confirmation
8. Setup reminders
```

**Implementation**:

```python
class BookingCreationWorkflow(Workflow):
    def __init__(self):
        super().__init__("booking_creation")
        self.add_step(ValidateBookingStep())
        self.add_step(CreateBookingStep())
        self.add_step(FindProvidersStep())
        self.add_step(NotifyProvidersStep())
        self.add_step(WaitForConfirmationStep())
        self.add_step(ScheduleAppointmentStep())
        self.add_step(SendConfirmationStep())
        self.add_step(SetupRemindersStep())
```

### 2. Provider Onboarding Workflow

```
Steps:
1. Collect provider information
2. Verify documents
3. Background check
4. Skills assessment
5. Training completion
6. Account activation
7. Welcome notification
```

### 3. Service Completion Workflow

```
Steps:
1. Mark service complete
2. Request customer feedback
3. Process payment
4. Update provider rating
5. Generate invoice
6. Archive booking
7. Trigger follow-up
```

## Advanced Features

### Conditional Steps

```python
class ConditionalStep(WorkflowStep):
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        if context.data.get("requires_approval"):
            # Execute approval logic
            await request_approval(context)
        else:
            # Skip approval
            self.state = WorkflowStepState.SKIPPED
        
        return context
```

### Parallel Execution (Future)

```python
class ParallelStep(WorkflowStep):
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Execute multiple tasks in parallel
        results = await asyncio.gather(
            task1(context),
            task2(context),
            task3(context)
        )
        
        context.data["results"] = results
        return context
```

### Retry Logic

```python
class RetryableStep(WorkflowStep):
    def __init__(self, max_retries=3):
        super().__init__("retryable_step")
        self.max_retries = max_retries
        self.retry_count = 0
    
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        while self.retry_count < self.max_retries:
            try:
                return await self._do_work(context)
            except Exception as e:
                self.retry_count += 1
                if self.retry_count >= self.max_retries:
                    raise
                await asyncio.sleep(2 ** self.retry_count)  # Exponential backoff
```

### Compensation (Rollback)

```python
class CompensatableStep(WorkflowStep):
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Store original state for rollback
        context.metadata["original_state"] = await get_current_state()
        
        # Execute step
        result = await self._do_work(context)
        return result
    
    async def compensate(self, context: WorkflowContext):
        """Rollback changes if workflow fails"""
        original_state = context.metadata.get("original_state")
        if original_state:
            await restore_state(original_state)
```

## Workflow Persistence (Future)

### Save Workflow State

```python
async def save_workflow_state(workflow: Workflow, context: WorkflowContext):
    """Persist workflow state to database"""
    await workflow_repository.save({
        "workflow_id": str(context.workflow_id),
        "workflow_name": workflow.name,
        "state": context.state,
        "data": context.data,
        "metadata": context.metadata,
        "current_step": workflow.current_step_index
    })
```

### Resume Workflow

```python
async def resume_workflow(workflow_id: str):
    """Resume a paused workflow"""
    # Load state from database
    state = await workflow_repository.get(workflow_id)
    
    # Reconstruct workflow
    workflow = create_workflow(state["workflow_name"])
    context = WorkflowContext(**state)
    
    # Resume from current step
    workflow.current_step_index = state["current_step"]
    result = await workflow.execute(context)
    
    return result
```

## Integration with Agents

### Agent as Workflow Step

```python
class AgentStep(WorkflowStep):
    def __init__(self, agent: BaseAgent):
        super().__init__(f"agent_{agent.name}")
        self.agent = agent
    
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Create agent task from context
        task = AgentTask(
            task_id=str(uuid4()),
            agent_type=self.agent.agent_type,
            input_data=context.data
        )
        
        # Execute agent
        response = await self.agent.process(task)
        
        # Update context with agent response
        context.data.update(response.output_data)
        
        return context

# Usage
workflow = Workflow("booking_with_agents")
workflow.add_step(AgentStep(matcher_agent))
workflow.add_step(AgentStep(negotiator_agent))
workflow.add_step(AgentStep(scheduler_agent))
```

## Integration with Events

### Emit Events from Workflow

```python
class EventEmittingWorkflow(Workflow):
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        # Emit workflow started event
        await event_bus.publish(BaseEvent(
            event_type=EventType.WORKFLOW_STARTED,
            source=self.name,
            payload={"workflow_id": str(context.workflow_id)}
        ))
        
        # Execute steps
        result = await super().execute(context)
        
        # Emit workflow completed event
        await event_bus.publish(BaseEvent(
            event_type=EventType.WORKFLOW_COMPLETED,
            source=self.name,
            payload={"workflow_id": str(context.workflow_id)}
        ))
        
        return result
```

### Trigger Workflow from Event

```python
async def handle_booking_created(event: BaseEvent):
    """Start workflow when booking is created"""
    booking_id = event.payload["booking_id"]
    
    # Create workflow
    workflow = BookingWorkflow()
    
    # Create context from event
    context = WorkflowContext(
        correlation_id=event.correlation_id,
        data=event.payload
    )
    
    # Execute workflow
    await workflow.execute(context)

# Subscribe
event_bus.subscribe(EventType.BOOKING_CREATED, handle_booking_created)
```

## Error Handling

### Workflow-Level Error Handling

```python
class ResilientWorkflow(Workflow):
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        try:
            return await super().execute(context)
        except Exception as e:
            # Log error
            logger.error("Workflow failed", 
                        workflow_id=str(context.workflow_id),
                        error=str(e))
            
            # Update context
            context.state = WorkflowState.FAILED
            context.error = str(e)
            
            # Emit failure event
            await event_bus.publish(BaseEvent(
                event_type=EventType.WORKFLOW_FAILED,
                source=self.name,
                payload={
                    "workflow_id": str(context.workflow_id),
                    "error": str(e)
                }
            ))
            
            # Attempt compensation
            await self.compensate(context)
            
            raise
```

## Testing Workflows

### Unit Testing Steps

```python
@pytest.mark.asyncio
async def test_find_providers_step():
    # Arrange
    step = FindProvidersStep()
    context = WorkflowContext(data={"booking_id": "123"})
    
    # Act
    result = await step.execute(context)
    
    # Assert
    assert "providers" in result.data
    assert len(result.data["providers"]) > 0
```

### Integration Testing Workflows

```python
@pytest.mark.asyncio
async def test_booking_workflow():
    # Arrange
    workflow = BookingWorkflow()
    context = WorkflowContext(
        data={
            "booking_id": "123",
            "customer_id": "456"
        }
    )
    
    # Act
    result = await workflow.execute(context)
    
    # Assert
    assert result.state == WorkflowState.COMPLETED
    assert "appointment_id" in result.data
```

## Best Practices

1. **Keep steps focused**: One step, one responsibility
2. **Make steps idempotent**: Safe to retry
3. **Handle errors gracefully**: Don't crash the workflow
4. **Use meaningful names**: Clear step and workflow names
5. **Log extensively**: Track workflow execution
6. **Test thoroughly**: Unit and integration tests
7. **Monitor performance**: Track execution time
8. **Version workflows**: Handle schema changes

## Future Enhancements

- **Visual workflow designer**: Drag-and-drop workflow creation
- **Workflow templates**: Reusable workflow patterns
- **Dynamic workflows**: Runtime workflow modification
- **Workflow analytics**: Execution metrics and insights
- **Distributed execution**: Scale across multiple workers
- **Workflow versioning**: Multiple versions in production

## Related Documentation

- [Architecture Overview](architecture.md)
- [Event System](event_system.md)
- [API Conventions](api_conventions.md)
