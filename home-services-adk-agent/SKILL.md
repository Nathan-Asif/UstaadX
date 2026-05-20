---
name: home-services-adk-agent
description: >
  Full implementation skill for a multi-agent home services booking system using
  Google ADK (Agent Development Kit) in Python. Use this skill whenever the user
  wants to build, implement, extend, or debug a multi-agent home services platform
  with agents for intent understanding, clarification, provider discovery, ranking,
  negotiation, booking, and follow-up. Triggers on: "build home services agent",
  "implement ADK multi-agent", "home services booking system", "plumber/AC/geyser
  booking agent", "provider ranking agent", "agentic booking flow", "ADK pipeline",
  "multi-agent handoff", or any mention of building a home services AI system with
  Google ADK. Always use this skill — do not attempt to build the ADK agent system
  without reading this file first.
---

# Home Services Multi-Agent System — Google ADK (Python)

A production-grade, 7-agent pipeline for home services booking. Covers Urdu/English
(Hinglish) intent understanding → provider discovery → Elo-ranked matching →
negotiation → booking → follow-up. Built on **Google ADK** with proper agent
handoffs, tool declarations, and system prompts.

---

## Quick Architecture Reference

```
User Message
    │
    ▼
[Agent 1: IntentUnderstandingAgent]  ← extracts service, location, urgency
    │  handoff_to_clarification() OR handoff_to_discovery()
    ▼
[Agent 2: ClarificationAgent]        ← asks missing info, re-triggers Agent 1
    │  handoff_to_discovery()
    ▼
[Agent 3: ProviderDiscoveryAgent]    ← Google Maps + DB lookup
    │  handoff_to_ranking()
    ▼
[Agent 4: RankingAgent]              ← Elo + weighted scoring
    │  handoff_to_negotiation()
    ▼
[Agent 5: NegotiationAgent]          ← confirms availability, timing
    │  handoff_to_booking()
    ▼
[Agent 6: BookingAgent]              ← generates booking record
    │  handoff_to_followup()
    ▼
[Agent 7: FollowUpAgent]             ← reminders, tracking, feedback
```

---

## Implementation Guide

### Step 1 — Install Dependencies

```bash
pip install google-adk google-generativeai pydantic python-dotenv httpx
```

Set environment variables:
```bash
GOOGLE_API_KEY=your_gemini_key
GOOGLE_MAPS_API_KEY=your_maps_key
```

---

### Step 2 — Project Structure

```
home_services/
├── main.py                  # ADK runner entry point
├── agents/
│   ├── __init__.py
│   ├── intent_agent.py      # Agent 1
│   ├── clarification_agent.py   # Agent 2
│   ├── discovery_agent.py   # Agent 3
│   ├── ranking_agent.py     # Agent 4
│   ├── negotiation_agent.py # Agent 5
│   ├── booking_agent.py     # Agent 6
│   └── followup_agent.py    # Agent 7
├── tools/
│   ├── __init__.py
│   ├── maps_tools.py        # Google Maps + Places
│   ├── db_tools.py          # Provider database
│   ├── elo_tools.py         # Elo scoring logic
│   └── booking_tools.py     # Booking generation
├── schemas/
│   ├── __init__.py
│   └── models.py            # Pydantic models
└── .env
```

---

### Step 3 — Pydantic Schemas (`schemas/models.py`)

Read → `references/schemas.md` for full Pydantic models.

Key schemas:
- `IntentOutput` — service_type, issue, priority, location, timing, confidence
- `ProviderRecord` — id, name, category, lat, lng, elo_score, ratings, availability
- `RankedProvider` — provider + composite_score + rank
- `BookingRecord` — booking_id, provider, user, service, timeline, status
- `FollowUpState` — booking_id, reminders_sent, completion_confirmed, feedback

---

### Step 4 — Tools Implementation

Read → `references/tools.md` for full tool code.

#### Tool Assignments Per Agent

| Agent | Tools Used |
|-------|-----------|
| IntentUnderstandingAgent | `detect_language`, `classify_service`, `extract_location_entity` |
| ClarificationAgent | `get_missing_fields`, `format_clarification_question` |
| ProviderDiscoveryAgent | `google_maps_nearby_search`, `filter_by_category`, `fetch_provider_availability` |
| RankingAgent | `calculate_elo_score`, `compute_proximity_score`, `compute_composite_score` |
| NegotiationAgent | `send_availability_request`, `negotiate_timing`, `get_provider_response` |
| BookingAgent | `generate_booking_id`, `create_booking_record`, `send_confirmation` |
| FollowUpAgent | `schedule_reminder`, `check_completion_status`, `collect_feedback`, `escalate_issue` |

---

### Step 5 — Agent Implementations

#### Agent 1 — IntentUnderstandingAgent (`agents/intent_agent.py`)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from schemas.models import IntentOutput
from tools.maps_tools import extract_location_entity
from tools.db_tools import classify_service

INTENT_SYSTEM_PROMPT = """
You are an intelligent Intent Understanding Agent for a home services platform
serving Pakistani users. Users speak in Urdu, English, or Hinglish.

Your ONLY job is to extract structured intent from the user's message.

## Extraction Rules
- service_type: One of [Plumbing, Electrical, AC/HVAC, Appliance Repair, Carpentry,
  Painting, Cleaning, Pest Control, Gas/Geyser, Internet/CCTV, Other]
- issue: Short description of the specific problem (e.g., "Leakage", "No cooling")
- priority: HIGH if emergency/urgent language detected, MEDIUM if same-day,
  LOW if flexible timing
- location: Extracted address/area. If missing → set to null
- timing: User's preferred time. If missing → set to null
- confidence: 0.0–1.0, your confidence in the extraction

## Urgency Keywords (Urdu/English)
HIGH → "leak", "leakage", "paani", "barq", "current aa raha", "aag", "blast",
        "emergency", "jaldi", "abhi", "foran"
MEDIUM → "aaj", "today", "jald", "soon"
LOW → "kal", "tomorrow", "koi bhi waqt", "flexible"

## Output Format
Always respond with ONLY valid JSON matching IntentOutput schema.
No extra text. No markdown.

## Examples
Input: "Geyser leak kar raha hai."
Output: {"service_type": "Gas/Geyser", "issue": "Leakage", "priority": "HIGH",
         "location": null, "timing": null, "confidence": 0.9}

Input: "AC theek karwana hai kal tak, Gulshan mein hoon"
Output: {"service_type": "AC/HVAC", "issue": "Repair needed", "priority": "MEDIUM",
         "location": "Gulshan, Karachi", "timing": "Tomorrow", "confidence": 0.95}
"""

def create_intent_agent() -> Agent:
    return Agent(
        name="IntentUnderstandingAgent",
        model="gemini-2.0-flash",
        description="Extracts service type, issue, priority, location, and timing from user messages in Urdu/English/Hinglish.",
        instruction=INTENT_SYSTEM_PROMPT,
        tools=[
            FunctionTool(classify_service),
            FunctionTool(extract_location_entity),
        ],
        output_key="intent",
    )
```

**Handoff Logic:**
- If `confidence < 0.6` OR `location is None` OR `service_type == "Other"` → handoff to `ClarificationAgent`
- Else → handoff to `ProviderDiscoveryAgent`

---

#### Agent 2 — ClarificationAgent (`agents/clarification_agent.py`)

```python
from google.adk.agents import Agent
from tools.db_tools import get_missing_fields, format_clarification_question

CLARIFICATION_SYSTEM_PROMPT = """
You are a friendly Clarification Agent for a home services platform.
A previous agent has extracted partial intent from the user. Your job is to
ask ONE clear, natural question to collect the single most important missing field.

## Rules
- Ask in the SAME language/style the user used (Urdu if they wrote Urdu, English if English)
- Ask only ONE question per turn — never multiple questions at once
- Be conversational, not robotic
- After getting the answer, extract the new info and pass back to IntentUnderstandingAgent

## Missing Field Priority (ask in this order)
1. location (most critical for provider search)
2. service_type (if still unclear)
3. timing (nice to have)

## Example Questions
- Location missing: "Aap kahan hain? Area ya address bata dein."
- AC type missing: "Aapka AC split hai ya window type?"
- Timing missing: "Kab chahiye? Aaj ya kal?"

## Output Format
Respond with the clarification question as plain conversational text.
"""

def create_clarification_agent() -> Agent:
    return Agent(
        name="ClarificationAgent",
        model="gemini-2.0-flash",
        description="Asks follow-up questions to collect missing intent fields from the user.",
        instruction=CLARIFICATION_SYSTEM_PROMPT,
        tools=[
            FunctionTool(get_missing_fields),
            FunctionTool(format_clarification_question),
        ],
        output_key="clarification_response",
    )
```

---

#### Agent 3 — ProviderDiscoveryAgent (`agents/discovery_agent.py`)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.maps_tools import google_maps_nearby_search
from tools.db_tools import filter_by_category, fetch_provider_availability

DISCOVERY_SYSTEM_PROMPT = """
You are a Provider Discovery Agent. Given a confirmed intent (service_type + location),
your job is to find all matching, available service providers nearby.

## Process
1. Use google_maps_nearby_search with the location and service_type keyword
2. Filter results by category match using filter_by_category
3. Fetch live availability for each matched provider
4. Return a list of candidate providers with their metadata

## Output Format
Return JSON array of ProviderRecord objects. Include:
- id, name, category, address, lat, lng
- elo_score (from database)
- rating (from database)
- distance_km (from Maps API)
- available: true/false
- available_slots (list of time strings if available)

## Rules
- Max 10 providers in output
- Only include providers where available == true
- If no providers found, set output to empty array and include "no_providers_found": true
"""

def create_discovery_agent() -> Agent:
    return Agent(
        name="ProviderDiscoveryAgent",
        model="gemini-2.0-flash",
        description="Finds nearby available home service providers using Google Maps and the provider database.",
        instruction=DISCOVERY_SYSTEM_PROMPT,
        tools=[
            FunctionTool(google_maps_nearby_search),
            FunctionTool(filter_by_category),
            FunctionTool(fetch_provider_availability),
        ],
        output_key="candidate_providers",
    )
```

---

#### Agent 4 — RankingAgent (`agents/ranking_agent.py`)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.elo_tools import calculate_elo_score, compute_proximity_score, compute_composite_score

RANKING_SYSTEM_PROMPT = """
You are a Provider Ranking Agent. You receive a list of candidate providers and
the original intent, then produce a ranked shortlist using weighted scoring.

## Ranking Formula
composite_score = (
    0.35 * elo_score_normalized +        # Meritocratic reliability
    0.20 * verified_rating_normalized +   # Customer feedback quality
    0.20 * proximity_score +              # Hyper-local distance
    0.10 * response_speed_score +         # Shadow agent response latency
    0.10 * urgency_match_score +          # Can handle HIGH priority if needed
    0.05 * lifecycle_completion_rate      # End-to-end job completion history
)

## Elo System Rules
- Base Elo: 1200 for new providers
- K-factor: 32 (calibrated by verified_rating — higher rating = lower K = more stable)
- Win = job completed successfully, rated ≥ 4 stars
- Loss = job cancelled, complained about, or rated ≤ 2 stars
- Update formula: new_elo = old_elo + K * (actual_score - expected_score)

## Urgency Match Rules
- If intent.priority == "HIGH": boost providers with urgency_capable == true by +0.15
- If intent.priority == "LOW": urgency_match_score = 1.0 for all (doesn't matter)

## Output Format
Return JSON: { "ranked_providers": [RankedProvider, ...], "top_pick": RankedProvider }
- ranked_providers: sorted descending by composite_score, max 5
- top_pick: the #1 ranked provider

## Notes
- Normalize all sub-scores to 0.0–1.0 before applying weights
- proximity_score = 1.0 - (distance_km / max_distance_km), clamp to [0, 1]
- elo_score_normalized = (elo - 800) / (2400 - 800), clamp to [0, 1]
"""

def create_ranking_agent() -> Agent:
    return Agent(
        name="RankingAgent",
        model="gemini-2.0-flash",
        description="Ranks candidate providers using Elo scores, proximity, ratings, response speed, and urgency match.",
        instruction=RANKING_SYSTEM_PROMPT,
        tools=[
            FunctionTool(calculate_elo_score),
            FunctionTool(compute_proximity_score),
            FunctionTool(compute_composite_score),
        ],
        output_key="ranked_providers",
    )
```

---

#### Agent 5 — NegotiationAgent (`agents/negotiation_agent.py`)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.db_tools import send_availability_request, negotiate_timing, get_provider_response

NEGOTIATION_SYSTEM_PROMPT = """
You are a Negotiation Agent. You contact the top-ranked provider on behalf of the
user to confirm availability and agree on timing.

## Process
1. Send availability request to the top_pick provider via send_availability_request
2. If provider responds AVAILABLE → confirm the earliest user-preferred slot
3. If provider responds UNAVAILABLE → try the 2nd ranked provider
4. Negotiate timing using negotiate_timing if user's preferred slot conflicts
5. Once agreed → pass confirmed assignment to BookingAgent

## Negotiation Rules
- Prefer the user's requested timing if possible
- If HIGH priority: accept any available slot within 2 hours
- If MEDIUM priority: negotiate within today's remaining slots
- If LOW priority: find earliest mutually convenient slot
- If ALL top-5 providers unavailable → return "no_provider_available" flag

## Communication Style
- Be firm but polite in negotiations
- Never reveal the user's maximum flexibility upfront
- Aim to confirm within 2 negotiation rounds

## Output Format
{
  "confirmed_provider": RankedProvider,
  "confirmed_time": "ISO datetime string",
  "negotiation_rounds": int,
  "negotiation_status": "confirmed" | "no_provider_available"
}
"""

def create_negotiation_agent() -> Agent:
    return Agent(
        name="NegotiationAgent",
        model="gemini-2.0-flash",
        description="Contacts ranked providers to confirm availability and negotiate job timing on behalf of the user.",
        instruction=NEGOTIATION_SYSTEM_PROMPT,
        tools=[
            FunctionTool(send_availability_request),
            FunctionTool(negotiate_timing),
            FunctionTool(get_provider_response),
        ],
        output_key="negotiation_result",
    )
```

---

#### Agent 6 — BookingAgent (`agents/booking_agent.py`)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.booking_tools import generate_booking_id, create_booking_record, send_confirmation

BOOKING_SYSTEM_PROMPT = """
You are a Booking Agent. You receive a confirmed provider + timing assignment and
generate a complete, official booking record.

## Booking Record Requirements
- booking_id: UUID format (use generate_booking_id)
- service_type, issue, priority from original intent
- provider: name, contact, address
- user: user_id or session_id
- confirmed_time: ISO datetime
- estimated_duration_minutes: based on service_type
- estimated_cost_pkr: range estimate based on service_type + historical data
- status: "CONFIRMED"
- created_at: current UTC timestamp

## Estimated Duration Reference
- Plumbing minor (leakage fix): 30–60 min
- AC service/cleaning: 60–90 min
- Electrical wiring: 90–180 min
- Geyser repair: 45–75 min
- Full appliance repair: 60–120 min

## Confirmation Message Format (in user's language)
"✅ Booking Confirmed!
Provider: [Name]
Service: [Service Type] — [Issue]
Time: [confirmed_time in readable format]
Estimated Cost: PKR [range]
Booking ID: [booking_id]"

## Output Format
{ "booking": BookingRecord, "confirmation_message": str }
"""

def create_booking_agent() -> Agent:
    return Agent(
        name="BookingAgent",
        model="gemini-2.0-flash",
        description="Generates official booking records, confirmations, and receipts after provider negotiation is complete.",
        instruction=BOOKING_SYSTEM_PROMPT,
        tools=[
            FunctionTool(generate_booking_id),
            FunctionTool(create_booking_record),
            FunctionTool(send_confirmation),
        ],
        output_key="booking_result",
    )
```

---

#### Agent 7 — FollowUpAgent (`agents/followup_agent.py`)

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.booking_tools import (
    schedule_reminder, check_completion_status,
    collect_feedback, escalate_issue
)

FOLLOWUP_SYSTEM_PROMPT = """
You are a Follow-Up Agent. You manage the post-booking lifecycle of a service job.

## Responsibilities
1. REMINDERS: Schedule reminders for the user (30 min before job) and provider (1 hour before)
2. STATUS TRACKING: Poll job status at scheduled_time + 30 min
3. COMPLETION CONFIRMATION: Ask user "Kaam ho gaya? (Was the job done?)"
4. FEEDBACK COLLECTION: After confirmation, ask for 1–5 star rating + optional comment
5. ESCALATION: If job not completed or rated ≤ 2 stars → escalate_issue

## Reminder Schedule
- T-60 min: Notify provider (via their registered channel)
- T-30 min: Notify user with provider contact details
- T+0: Mark as "IN_PROGRESS"
- T+estimated_duration+15: Check completion status

## Feedback Flow
After user confirms completion:
"Job complete! Please rate [Provider Name]: ⭐1–5
(Optional: Kuch kehna chahte hain? / Any feedback?)"

## Escalation Triggers
- User says job NOT done at T+estimated_duration+30
- Rating ≤ 2 stars
- Provider marked as no-show

## Elo Update (trigger after feedback)
- On success (rating ≥ 4): call elo_update(provider_id, result="win")
- On failure (rating ≤ 2): call elo_update(provider_id, result="loss")

## Output Format
{
  "followup_status": "completed" | "escalated" | "pending",
  "rating_collected": int | null,
  "feedback_text": str | null,
  "elo_updated": bool
}
"""

def create_followup_agent() -> Agent:
    return Agent(
        name="FollowUpAgent",
        model="gemini-2.0-flash",
        description="Manages post-booking reminders, job status tracking, feedback collection, and Elo score updates.",
        instruction=FOLLOWUP_SYSTEM_PROMPT,
        tools=[
            FunctionTool(schedule_reminder),
            FunctionTool(check_completion_status),
            FunctionTool(collect_feedback),
            FunctionTool(escalate_issue),
        ],
        output_key="followup_result",
    )
```

---

### Step 6 — Orchestrator Pipeline (`main.py`)

Read → `references/orchestrator.md` for the full pipeline with handoff logic.

Key pattern:

```python
from google.adk.agents import SequentialAgent, Agent
from agents.intent_agent import create_intent_agent
# ... import all agents

def build_pipeline() -> SequentialAgent:
    return SequentialAgent(
        name="HomeServicesPipeline",
        description="End-to-end home services booking pipeline",
        sub_agents=[
            create_intent_agent(),
            create_clarification_agent(),   # conditional
            create_discovery_agent(),
            create_ranking_agent(),
            create_negotiation_agent(),
            create_booking_agent(),
            create_followup_agent(),
        ],
    )
```

For **conditional handoffs** (Intent → Clarification vs Discovery), use ADK's
`LlmAgent` with a routing tool, or use `output_key` checks in a custom
`SequentialAgent` subclass. See `references/orchestrator.md` for the full
conditional routing pattern.

---

### Step 7 — Running the System

```python
# main.py
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

async def main():
    pipeline = build_pipeline()
    session_service = InMemorySessionService()
    runner = Runner(
        agent=pipeline,
        app_name="home_services",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="home_services",
        user_id="user_001"
    )

    user_input = "Geyser leak kar raha hai, DHA Phase 5 mein hoon"

    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message={"role": "user", "parts": [{"text": user_input}]},
    ):
        if event.is_final_response():
            print(event.content)

asyncio.run(main())
```

---

## Reference Files

| File | Contents |
|------|----------|
| `references/schemas.md` | Full Pydantic models for all data structures |
| `references/tools.md` | Full implementation of all 15+ tool functions |
| `references/orchestrator.md` | Full pipeline with conditional routing + handoff patterns |

---

## Common Mistakes to Avoid

1. **Don't share state via global variables** — use ADK's `output_key` / session state
2. **Don't skip the Elo update** — FollowUpAgent must call `elo_update` after feedback
3. **ClarificationAgent loops back** — after getting the answer, re-invoke IntentAgent (not DiscoveryAgent directly)
4. **All tools must be `FunctionTool` wrapped** — raw functions won't register in ADK
5. **Use `gemini-2.0-flash` not `gemini-pro`** — ADK is optimized for Flash models
