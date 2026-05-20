# pyrefly: ignore [missing-import]
from google.adk.agents import Agent
# pyrefly: ignore [missing-import]
from google.adk.tools import FunctionTool
from app.tools.elo_tools import calculate_elo_score, compute_proximity_score, compute_composite_score

RANKING_SYSTEM_PROMPT = """
## Context
You are a Provider Ranking Agent. You receive a list of candidate providers and the original intent. Your goal is to produce a ranked shortlist using weighted scoring.

## Constraints
- Apply the Ranking Formula:
  composite_score = (0.35 * elo_norm) + (0.20 * rating_norm) + (0.20 * proximity) + (0.10 * speed_norm) + (0.10 * urgency_match) + (0.05 * lifecycle_norm)
- Output MUST be valid JSON.
- Output MUST contain exactly: { "ranked_providers": [RankedProvider, ...], "top_pick": RankedProvider }.
- "ranked_providers" must be sorted descending by composite_score, max 5.
- "top_pick" is the #1 ranked provider.

## Clarity
Normalize sub-scores to [0.0, 1.0] before weighting.
urgency_match = 1.0 if capable or priority!=HIGH, else 0.3.
Ensure accurate calculation.
"""

def create_ranking_agent() -> Agent:
    return Agent(
        name="RankingAgent",
        model="gemini-2.0-flash",
        description="Ranks candidate providers using Elo scores, proximity, ratings, response speed, and urgency match.",
        instruction=RANKING_SYSTEM_PROMPT,
        tools=[
            FunctionTool(calculate_elo_score),
            FunctionTool(compute_proximity_score),
            FunctionTool(compute_composite_score),
        ],
        output_key="ranked_providers",
    )
