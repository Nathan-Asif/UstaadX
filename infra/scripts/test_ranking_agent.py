import sys
import asyncio
import os
from pathlib import Path

# Add backend_api to Python path so we can import app modules
backend_dir = Path(__file__).parent.parent.parent / "apps" / "backend_api"
sys.path.insert(0, str(backend_dir))

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# pyrefly: ignore [missing-import]
from app.core.config import settings
# pyrefly: ignore [missing-import]
from app.agents.ranking_agent import create_ranking_agent

async def test_ranking_agent():
    # Make sure we have the API key
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
    
    agent = create_ranking_agent()
    
    # ADK requires a runner to execute the agent and maintain memory/session
    runner = Runner(
        app_name="RankingTest",
        agent=agent,
        session_service=InMemorySessionService()
    )
    
    prompt = """
    Rank technicians for the following task context:
    {"customer_id": "11111111-1111-1111-1111-111111111111", "city": "Karachi", "problem_description": "My AC is leaking water heavily and stopped cooling. Need someone urgently, guests are arriving soon!"}
    """
    
    message = types.Content(role="user", parts=[types.Part.from_text(prompt)])
    
    print("Sending test task to ADK RankingAgent via Runner...")
    try:
        # Run the agent through the runner
        async for event in runner.run_async(
            user_id="test_user",
            session_id="test_session",
            new_message=message
        ):
            # Print each event as it happens (tool calls, reasoning, etc)
            print("Event:", event)
            
    except Exception as e:
        print("\nFAILED:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ranking_agent())
