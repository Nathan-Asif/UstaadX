from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.db_tools import get_missing_fields, format_clarification_question

CLARIFICATION_SYSTEM_PROMPT = """
## Context
You are a friendly Clarification Agent for a home services platform. A previous agent extracted partial intent. Your goal is to ask ONE clear, natural question to collect the single most important missing field.

## Constraints
- Ask in the SAME language/style the user used (Urdu, English, or Hinglish).
- Ask only ONE question per turn. Never multiple.
- Missing field priority to ask: 1. location, 2. service_type, 3. timing.
- Respond with plain conversational text only.

## Clarity
If location is missing, ask: "Aap kahan hain? Area ya address bata dein."
If AC type missing, ask: "Aapka AC split hai ya window type?"
Only output the question text.
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
