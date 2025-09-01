# orquestra/models/primitives.py
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Agent(BaseModel):
    """Represents a configured AI agent."""

    name: str = Field(
        ..., description="A unique identifier for the agent in the workflow."
    )
    provider: str = Field(
        ..., description="The AI provider, e.g., 'openai', 'anthropic'."
    )
    model: str = Field(
        ...,
        description="The specific model name, e.g., 'gpt-5', 'claude-opus-4-1-20250805'.",
    )


class Task(BaseModel):
    """Represents a single task to be executed by an agent."""

    name: str = Field(
        ..., description="A unique identifier for the task in the workflow."
    )
    agent: str = Field(..., description="The name of the agent assigned to this task.")
    instruction: str = Field(
        ..., description="The primary instruction or prompt for the agent."
    )
    # We use a dictionary for inputs for maximum flexibility
    inputs: Dict[str, Any] = Field(
        default_factory=dict,
        description="A dictionary of key-value inputs for the instruction.",
    )
    depends_on: List[str] = Field(
        default_factory=list,
        description="A list of task names that must be completed before this one starts.",
    )


class Workflow(BaseModel):
    """Represents a complete, multi-step workflow."""

    name: str = Field(..., description="The name of the workflow.")
    description: Optional[str] = Field(
        None, description="An optional description of the workflow's purpose."
    )
    agents: List[Agent] = Field(
        ..., description="A list of all agents available in this workflow."
    )
    tasks: List[Task] = Field(..., description="The sequence of tasks to execute.")
