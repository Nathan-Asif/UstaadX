import asyncio
import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import agent_tool

# Ensure to load env vars for ADK
from dotenv import load_dotenv
load_dotenv()

from app.agents.intent_agent import create_intent_agent
from app.agents.clarification_agent import create_clarification_agent
from app.agents.discovery_agent import create_discovery_agent
from app.agents.ranking_agent import create_ranking_agent
from app.agents.negotiation_agent import create_negotiation_agent
from app.agents.booking_agent import create_booking_agent
from app.agents.followup_agent import create_followup_agent


def build_pipeline() -> LlmAgent:
    """
    Build the full 7-agent pipeline with conditional routing.
    
    Flow:
      IntentAgent → [ClarificationAgent?] → DiscoveryAgent → RankingAgent
      → NegotiationAgent → BookingAgent → FollowUpAgent
    """

    # ── Agents ────────────────────────────────────────────────────────────────
    intent_agent = create_intent_agent()
    clarification_agent = create_clarification_agent()
    discovery_agent = create_discovery_agent()
    ranking_agent = create_ranking_agent()
    negotiation_agent = create_negotiation_agent()
    booking_agent = create_booking_agent()
    followup_agent = create_followup_agent()

    # ── Post-Discovery Linear Pipeline ────────────────────────────────────────
    # These always run sequentially after discovery
    post_discovery = SequentialAgent(
        name="PostDiscoveryPipeline",
        description="Ranks providers, negotiates, books, and follows up.",
        sub_agents=[
            ranking_agent,
            negotiation_agent,
            booking_agent,
            followup_agent,
        ],
    )

    # ── Root Orchestrator ──────────────────────────────────────────────────────
    # LlmAgent with access to all agents as tools, decides routing
    root = LlmAgent(
        name="HomeServiceOrchestrator",
        model="gemini-2.0-flash",
        description="Root orchestrator for home services booking pipeline.",
        instruction="""
You are the master orchestrator for a home services booking system.

## Your Job
Route the user's request through the correct sequence of specialist agents.

## Routing Logic

### Step 1 — Always call IntentUnderstandingAgent first.

### Step 2 — Check intent output:
- If `confidence < 0.6` OR `location is null` OR `service_type == "Other"`:
  → call ClarificationAgent, then re-call IntentUnderstandingAgent
- Else:
  → proceed directly to ProviderDiscoveryAgent

### Step 3 — After discovery, always run the PostDiscoveryPipeline:
  ProviderDiscoveryAgent → RankingAgent → NegotiationAgent → BookingAgent → FollowUpAgent

### Step 4 — Handle edge cases:
- If negotiation_status == "no_provider_available":
  Inform user: "Sorry, koi provider available nahi hai. Baad mein try karein."
  Stop the pipeline.
- If candidate_providers is empty:
  Inform user: "Is area mein koi provider nahi mila."
  Stop the pipeline.

## Rules
- Never skip IntentUnderstandingAgent
- Never call BookingAgent before NegotiationAgent
- Always call FollowUpAgent after successful booking
- Respond to user in the SAME language they used
""",
        sub_agents=[
            intent_agent,
            clarification_agent,
            discovery_agent,
            post_discovery,
        ],
    )

    return root


async def run_pipeline(user_message: str, user_id: str = "user_001"):
    """Run the full pipeline for a user message."""

    pipeline = build_pipeline()
    session_service = InMemorySessionService()

    runner = Runner(
        agent=pipeline,
        app_name="home_services_booking",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="home_services_booking",
        user_id=user_id,
    )

    print(f"\n{'='*60}")
    print(f"User: {user_message}")
    print(f"{'='*60}")

    from google.genai import types
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=types.Content(role="user", parts=[types.Part.from_text(text=user_message)]),
    ):
        # Print agent activity for debugging
        if hasattr(event, "author") and event.author:
            print(f"\n[{event.author}]")

        if event.is_final_response():
            print(f"\n✅ Final Response:\n{event.content.parts[0].text}")
            return event

    return None


if __name__ == "__main__":
    # Test cases
    test_messages = [
        "Geyser leak kar raha hai, DHA Phase 5 mein hoon",
        "AC theek karwana hai kal tak",       # Missing location → triggers clarification
        "Bijli ka masla hai foran theek karo, PECHS Block 2",
    ]

    for msg in test_messages:
        asyncio.run(run_pipeline(msg))
        print("\n" + "─"*60 + "\n")
