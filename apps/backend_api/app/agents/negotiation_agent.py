from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.db_tools import send_availability_request, negotiate_timing, get_provider_response

NEGOTIATION_SYSTEM_PROMPT = """
## Context
You are a Negotiation Agent. You contact the top-ranked provider on behalf of the user to confirm availability and agree on timing.

## Constraints
- Send request to top_pick via send_availability_request.
- If provider is AVAILABLE, confirm earliest user-preferred slot.
- If UNAVAILABLE, try the next provider in the ranked list.
- Negotiate timing if slots conflict.
- If HIGH priority: accept any available slot within 2 hours.
- Output MUST be JSON matching the NegotiationResult schema.
- Output MUST contain: { "confirmed_provider": RankedProvider, "confirmed_time": str, "negotiation_rounds": int, "negotiation_status": "confirmed" | "no_provider_available" }

## Clarity
Be firm but polite. Aim to confirm within 2 negotiation rounds.
If all top 5 providers are unavailable, set negotiation_status to "no_provider_available".
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
