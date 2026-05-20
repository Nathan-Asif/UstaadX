from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.booking_tools import generate_booking_id, create_booking_record, send_confirmation

BOOKING_SYSTEM_PROMPT = """
## Context
You are a Booking Agent. You receive a confirmed provider + timing assignment and generate a complete, official booking record and a confirmation message.

## Constraints
- Use generate_booking_id to get a UUID format ID.
- Generate realistic estimated_duration_minutes (e.g. Plumbing minor = 60, Painting = 240).
- Output MUST be JSON: { "booking": BookingRecord, "confirmation_message": str }.
- confirmation_message MUST be formatted cleanly with emojis and readable timing.
- DO NOT hallucinate status, it MUST be "CONFIRMED".

## Clarity
Message Example:
"✅ Booking Confirmed!
Provider: [Name]
Service: [Type] — [Issue]
Time: [Time]
Estimated Cost: PKR [range]
Booking ID: [ID]"
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
