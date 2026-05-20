import os
import sys
import asyncio

# Add the backend_api directory to the python path so the 'app' module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../apps/backend_api')))

# pyrefly: ignore [missing-import]
from app.core.config import settings
from google.adk.agents import Agent

async def main():
    agent = Agent(
        name="Test",
        model="gemini-2.5-flash",
        instruction="Say hi",
    )
    print("Agent methods:", [m for m in dir(agent) if not m.startswith("_")])

if __name__ == "__main__":
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
    asyncio.run(main())
