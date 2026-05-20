from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class TaskContext(BaseModel):
    """Input context from the customer request."""
    customer_id: UUID
    city: str
    problem_description: str
    preferred_time: Optional[str] = None

class ParsedTask(BaseModel):
    """The AI-parsed understanding of the task."""
    required_skills: List[str]
    urgency_level: str # HIGH, MEDIUM, LOW
    task_difficulty_elo: int # integer rating from 1000 to 2000
    reasoning: str

class TechnicianProfile(BaseModel):
    """Technician data loaded from the database."""
    id: UUID
    name: str
    base_elo: int
    skills: List[str]
    is_active: bool

class RankedTechnician(BaseModel):
    """A technician scored against the specific task."""
    technician: TechnicianProfile
    expected_performance: float # The mathematical 'E' score (0 to 1)
    match_reasoning: str

class RankingResponse(BaseModel):
    """The final output payload from the Ranking Agent."""
    parsed_task: ParsedTask
    ranked_technicians: List[RankedTechnician]
