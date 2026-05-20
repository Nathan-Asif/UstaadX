# Schemas Reference — Home Services ADK Agent

## `schemas/models.py`

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
import uuid


# ─── Intent ───────────────────────────────────────────────────────────────────

class IntentOutput(BaseModel):
    service_type: Literal[
        "Plumbing", "Electrical", "AC/HVAC", "Appliance Repair",
        "Carpentry", "Painting", "Cleaning", "Pest Control",
        "Gas/Geyser", "Internet/CCTV", "Other"
    ]
    issue: str = Field(..., description="Short description of the problem")
    priority: Literal["HIGH", "MEDIUM", "LOW"]
    location: Optional[str] = None
    timing: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)


# ─── Provider ─────────────────────────────────────────────────────────────────

class AvailableSlot(BaseModel):
    slot_time: str  # ISO datetime string
    duration_minutes: int


class ProviderRecord(BaseModel):
    id: str
    name: str
    category: str
    address: str
    lat: float
    lng: float
    phone: str
    elo_score: float = Field(default=1200.0)
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    rating_count: int = Field(default=0)
    distance_km: float
    available: bool
    available_slots: List[AvailableSlot] = []
    urgency_capable: bool = False
    lifecycle_completion_rate: float = Field(default=0.0, ge=0.0, le=1.0)
    response_speed_ms: int = Field(default=5000, description="Shadow agent avg response latency")


class RankedProvider(BaseModel):
    provider: ProviderRecord
    composite_score: float
    rank: int
    score_breakdown: dict  # {elo: float, rating: float, proximity: float, speed: float, urgency: float, lifecycle: float}


# ─── Negotiation ──────────────────────────────────────────────────────────────

class NegotiationResult(BaseModel):
    confirmed_provider: RankedProvider
    confirmed_time: str  # ISO datetime
    negotiation_rounds: int
    negotiation_status: Literal["confirmed", "no_provider_available"]


# ─── Booking ──────────────────────────────────────────────────────────────────

class BookingRecord(BaseModel):
    booking_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    service_type: str
    issue: str
    priority: str
    provider_id: str
    provider_name: str
    provider_phone: str
    provider_address: str
    user_id: str
    confirmed_time: str
    estimated_duration_minutes: int
    estimated_cost_pkr_min: int
    estimated_cost_pkr_max: int
    status: Literal["PENDING", "CONFIRMED", "IN_PROGRESS", "COMPLETED", "CANCELLED", "ESCALATED"]
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# ─── Follow-Up ────────────────────────────────────────────────────────────────

class FollowUpState(BaseModel):
    booking_id: str
    reminders_sent: List[str] = []  # list of reminder types sent
    job_status: Literal["CONFIRMED", "IN_PROGRESS", "COMPLETED", "ESCALATED"] = "CONFIRMED"
    completion_confirmed: bool = False
    rating_collected: Optional[int] = None  # 1–5
    feedback_text: Optional[str] = None
    elo_updated: bool = False
    escalation_reason: Optional[str] = None


# ─── Pipeline State (shared across agents via ADK session) ────────────────────

class PipelineState(BaseModel):
    """Stored in ADK session state. Each agent reads/writes its section."""
    user_id: str
    session_id: str
    raw_message: str
    intent: Optional[IntentOutput] = None
    clarification_needed: bool = False
    clarification_response: Optional[str] = None
    candidate_providers: List[ProviderRecord] = []
    ranked_providers: List[RankedProvider] = []
    top_pick: Optional[RankedProvider] = None
    negotiation_result: Optional[NegotiationResult] = None
    booking: Optional[BookingRecord] = None
    followup: Optional[FollowUpState] = None
```
