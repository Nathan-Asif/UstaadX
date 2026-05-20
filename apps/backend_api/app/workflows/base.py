"""
Workflow Engine - Base abstractions for orchestration
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class WorkflowState(str, Enum):
    """Workflow execution states"""

    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class WorkflowStepState(str, Enum):
    """Individual step states"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowContext(BaseModel):
    """Context passed through workflow execution"""

    workflow_id: UUID = Field(default_factory=uuid4)
    state: WorkflowState = WorkflowState.PENDING
    data: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    error: Optional[str] = None


class WorkflowStep(ABC):
    """Base class for workflow steps"""

    def __init__(self, name: str):
        self.name = name
        self.state = WorkflowStepState.PENDING

    @abstractmethod
    async def execute(self, context: WorkflowContext) -> WorkflowContext:
        """Execute the workflow step"""
        pass

    async def on_success(self, context: WorkflowContext):
        """Hook called on successful execution"""
        pass

    async def on_failure(self, context: WorkflowContext, error: Exception):
        """Hook called on execution failure"""
        pass


class Workflow(ABC):
    """Base class for workflows"""

    def __init__(self, name: str):
        self.name = name
        self.steps: list[WorkflowStep] = []

    def add_step(self, step: WorkflowStep):
        """Add a step to the workflow"""
        self.steps.append(step)

    async def execute(self, initial_context: Optional[WorkflowContext] = None) -> WorkflowContext:
        """Execute the workflow"""
        context = initial_context or WorkflowContext()
        context.state = WorkflowState.RUNNING

        for step in self.steps:
            try:
                step.state = WorkflowStepState.RUNNING
                context = await step.execute(context)
                step.state = WorkflowStepState.COMPLETED
                await step.on_success(context)
            except Exception as e:
                step.state = WorkflowStepState.FAILED
                context.state = WorkflowState.FAILED
                context.error = str(e)
                await step.on_failure(context, e)
                raise

        context.state = WorkflowState.COMPLETED
        return context
