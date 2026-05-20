"""
Agent System - Base abstractions for AI agents
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AgentType(str, Enum):
    """Types of agents in the system"""

    MATCHER = "matcher"  # Matches customers with providers
    NEGOTIATOR = "negotiator"  # Handles price negotiation
    SCHEDULER = "scheduler"  # Manages scheduling and timing
    FOLLOWUP = "followup"  # Handles follow-up communications
    QUALITY_CHECKER = "quality_checker"  # Quality assurance
    COORDINATOR = "coordinator"  # Orchestrates multiple agents


class AgentTask(BaseModel):
    """Task assigned to an agent"""

    task_id: str
    agent_type: AgentType
    input_data: Dict[str, Any]
    context: Dict[str, Any] = {}
    priority: int = 0


class AgentResponse(BaseModel):
    """Response from an agent"""

    task_id: str
    success: bool
    output_data: Dict[str, Any]
    metadata: Dict[str, Any] = {}
    error: Optional[str] = None


class BaseAgent(ABC):
    """Base class for all AI agents"""

    def __init__(self, agent_type: AgentType, name: str):
        self.agent_type = agent_type
        self.name = name

    @abstractmethod
    async def process(self, task: AgentTask) -> AgentResponse:
        """Process a task and return response"""
        pass

    async def validate_input(self, task: AgentTask) -> bool:
        """Validate task input before processing"""
        return True

    async def on_success(self, response: AgentResponse):
        """Hook called on successful task completion"""
        pass

    async def on_failure(self, task: AgentTask, error: Exception):
        """Hook called on task failure"""
        pass
