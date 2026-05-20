import math
from typing import List
from app.agents.base import BaseAgent, AgentTask, AgentResponse, AgentType
from app.schemas.ranking import TaskContext, ParsedTask, TechnicianProfile, RankedTechnician, RankingResponse
from app.services.llm_service import llm_service
from app.db.supabase import supabase_client

class RankingAgent(BaseAgent):
    """
    Agent 4: Ranking Agent (Elo System)
    Parses customer context via Gemini, scores task difficulty, and ranks technicians using the Expected Performance formula.
    """
    def __init__(self):
        super().__init__(agent_type=AgentType.MATCHER, name="Ranking Agent (Elo System)")

    async def validate_input(self, task: AgentTask) -> bool:
        """Ensure input_data has required fields."""
        required = ["customer_id", "city", "problem_description"]
        return all(k in task.input_data for k in required)

    async def process(self, task: AgentTask) -> AgentResponse:
        try:
            # 1. Parse Input Context
            context = TaskContext(**task.input_data)

            # 2. Use Gemini LLM to determine Task Difficulty Elo and extract skills
            prompt = f"""
            You are the UstaadX AI logic engine.
            A customer in {context.city} reported the following issue: "{context.problem_description}"
            
            Analyze this issue and return a strict JSON response with the following keys:
            - "required_skills": List of standard technical skills needed (e.g., ["AC Repair", "Plumbing", "Electrician", "Refrigerator Repair"]). Use the best match.
            - "urgency_level": "HIGH", "MEDIUM", or "LOW".
            - "task_difficulty_elo": An integer rating from 1000 to 2000 representing how difficult this task is. 1000 is basic, 1500 is intermediate, 2000 is expert/emergency level.
            - "reasoning": A brief 1-sentence explanation for the chosen Elo and urgency.
            """
            
            # Fetch structured JSON from Gemini
            llm_result = await llm_service.generate_json_response(prompt)
            parsed_task = ParsedTask(**llm_result)

            # 3. Query available technicians from Supabase
            # We fetch all active technicians and then filter in memory for simplicity (MVP)
            response = supabase_client.table("technicians").select("*").eq("is_active", True).execute()
            all_techs = response.data
            
            # Filter techs in the requested city
            city_techs = [t for t in all_techs if t.get("location", {}).get("city", "").lower() == context.city.lower()]
            
            # Filter techs matching at least one required skill
            matched_techs = []
            for t in city_techs:
                tech_skills = set(t.get("skills", []))
                req_skills = set(parsed_task.required_skills)
                # We include the tech if there's any skill intersection or if Gemini couldn't parse any specific skills
                if tech_skills.intersection(req_skills) or not req_skills:
                    matched_techs.append(TechnicianProfile(**t))

            # 4. Calculate Expected Performance (E) using the Elo formula
            # Formula: E = 1 / (1 + 10 ^ ((Task_Rating - Technician_Elo) / 400))
            ranked_list: List[RankedTechnician] = []
            for tech in matched_techs:
                e_score = 1 / (1 + math.pow(10, (parsed_task.task_difficulty_elo - tech.base_elo) / 400.0))
                
                reason = f"{tech.name} has Elo {tech.base_elo} vs Task Elo {parsed_task.task_difficulty_elo}. Expected success probability is {e_score*100:.1f}%."
                
                ranked_list.append(RankedTechnician(
                    technician=tech,
                    expected_performance=e_score,
                    match_reasoning=reason
                ))

            # 5. Sort by Expected Performance (descending) so top matches are first
            ranked_list.sort(key=lambda x: x.expected_performance, reverse=True)

            output = RankingResponse(
                parsed_task=parsed_task,
                ranked_technicians=ranked_list
            )

            return AgentResponse(
                task_id=task.task_id,
                success=True,
                output_data=output.model_dump(mode="json")
            )

        except Exception as e:
            return AgentResponse(
                task_id=task.task_id,
                success=False,
                output_data={},
                error=str(e)
            )
