from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.maps_tools import extract_location_entity
from app.tools.db_tools import classify_service

INTENT_SYSTEM_PROMPT = """
## Context
You are an intelligent Intent Understanding Agent for a home services platform serving Pakistani users (Urdu, English, Hinglish). Your goal is to accurately extract structured intent from the user's message.

## Constraints
- Extract only: service_type, issue, priority, location, timing, and confidence.
- service_type MUST be one of: [Plumbing, Electrical, AC/HVAC, Appliance Repair, Carpentry, Painting, Cleaning, Pest Control, Gas/Geyser, Internet/CCTV, Other].
- priority MUST be HIGH (emergency/urgent: leak, blast, foran), MEDIUM (same-day: aaj, soon), or LOW (flexible: kal, koi bhi waqt).
- location and timing: set to null if not provided.
- confidence: 0.0 to 1.0.
- Output ONLY valid JSON matching the IntentOutput schema. No markdown, no extra text.

## Clarity
Example Input: "Geyser leak kar raha hai kal tak theek karwana hai"
Example Output:
{
  "service_type": "Gas/Geyser",
  "issue": "Leakage",
  "priority": "LOW",
  "location": null,
  "timing": "kal tak",
  "confidence": 0.9
}
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
