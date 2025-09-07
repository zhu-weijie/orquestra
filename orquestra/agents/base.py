from abc import ABC, abstractmethod

from orquestra.models import Agent


class BaseAgentExecutor(ABC):
    """Abstract base class for all agent executors."""

    @abstractmethod
    def execute(self, agent: Agent, instruction: str) -> str:
        """
        Executes a task with the given agent and instruction.

        Args:
            agent: The Agent model instance.
            instruction: The rendered instruction for the agent.

        Returns:
            The string output from the agent.
        """
        pass
