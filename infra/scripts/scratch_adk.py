import os
from google.adk.agents import Agent
import asyncio

async def main():
    agent = Agent(
        name="Test",
        model="gemini-2.5-flash",
        instruction="Say hi",
    )
    print("Agent methods:", [m for m in dir(agent) if not m.startswith("_")])

if __name__ == "__main__":
    os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6K3nJv79efPIBDewgWkuK-WhGT036rOq8Yb0JBuo-K8qA"
    asyncio.run(main())
