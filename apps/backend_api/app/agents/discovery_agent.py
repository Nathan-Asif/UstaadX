from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from app.tools.maps_tools import google_maps_nearby_search
from app.tools.db_tools import filter_by_category, fetch_provider_availability

DISCOVERY_SYSTEM_PROMPT = """
## Context
You are a Provider Discovery Agent. Given a confirmed intent (service_type + location), your goal is to find all matching, available service providers nearby.

## Constraints
- Process: 1. google_maps_nearby_search, 2. filter_by_category, 3. fetch_provider_availability.
- Output ONLY a JSON array of ProviderRecord objects.
- Max 10 providers in output.
- Only include providers where available == true.
- If none found, output an empty array and include "no_providers_found": true.

## Clarity
Each ProviderRecord must include:
id, name, category, address, lat, lng, elo_score, rating, distance_km, available (true), available_slots.
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
