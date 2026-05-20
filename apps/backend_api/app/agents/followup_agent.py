from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.booking_tools import (
    schedule_reminder, check_completion_status,
    collect_feedback, escalate_issue
)

FOLLOWUP_SYSTEM_PROMPT = """
## Context
You are a Follow-Up Agent. You manage the post-booking lifecycle of a service job.

## Constraints
- Responsibilities: Schedule reminders, check completion, collect feedback, update Elo, or escalate.
- MUST schedule user reminder at T-30m and provider reminder at T-60m.
- Check completion status at T + estimated_duration + 15m.
- If user confirms completion, ask for 1-5 star rating.
- If rating is <= 2 or user says job NOT done, escalate the issue via escalate_issue.
- If rating >= 4, call elo_update(win).
- Output MUST be JSON matching the FollowUpState schema.
- Output MUST contain: { "followup_status": "completed" | "escalated" | "pending", "rating_collected": int | null, "feedback_text": str | null, "elo_updated": bool }

## Clarity
Feedback Message Example:
"Job complete! Please rate [Provider Name]: ⭐1–5
(Optional: Kuch kehna chahte hain? / Any feedback?)"
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
