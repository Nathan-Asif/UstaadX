"""
Base Event System - Foundation for event-driven architecture
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """System-wide event types"""

    # Booking Events
    BOOKING_CREATED = "booking.created"
    BOOKING_UPDATED = "booking.updated"
    BOOKING_CANCELLED = "booking.cancelled"
    BOOKING_COMPLETED = "booking.completed"

    # Provider Events
    PROVIDER_MATCHED = "provider.matched"
    PROVIDER_CONFIRMED = "provider.confirmed"
    PROVIDER_REJECTED = "provider.rejected"
    PROVIDER_ARRIVED = "provider.arrived"

    # Negotiation Events
    NEGOTIATION_STARTED = "negotiation.started"
    NEGOTIATION_OFFER_MADE = "negotiation.offer_made"
    NEGOTIATION_ACCEPTED = "negotiation.accepted"
    NEGOTIATION_REJECTED = "negotiation.rejected"

    # Workflow Events
    WORKFLOW_STARTED = "workflow.started"
    WORKFLOW_STEP_COMPLETED = "workflow.step_completed"
    WORKFLOW_COMPLETED = "workflow.completed"
    WORKFLOW_FAILED = "workflow.failed"

    # Agent Events
    AGENT_TASK_ASSIGNED = "agent.task_assigned"
    AGENT_TASK_COMPLETED = "agent.task_completed"
    AGENT_TASK_FAILED = "agent.task_failed"

    # Follow-up Events
    FOLLOWUP_TRIGGERED = "followup.triggered"
    FOLLOWUP_COMPLETED = "followup.completed"

    # System Events
    SYSTEM_ERROR = "system.error"
    SYSTEM_NOTIFICATION = "system.notification"


class BaseEvent(BaseModel):
    """Base class for all events in the system"""

    event_id: UUID = Field(default_factory=uuid4)
    event_type: EventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str  # Service/component that emitted the event
    correlation_id: Optional[UUID] = None  # For tracing related events
    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }
