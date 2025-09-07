from anthropic import Anthropic

from orquestra.models import Agent

from .base import BaseAgentExecutor


class AnthropicAgentExecutor(BaseAgentExecutor):
    """An agent executor for Anthropic's Claude models."""

    def __init__(self):
        # The client will automatically look for the ANTHROPIC_API_KEY
        # environment variable.
        self.client = Anthropic()

    def execute(self, agent: Agent, instruction: str) -> str:
        """Executes a task using the Anthropic API."""
        message = self.client.messages.create(
            model=agent.model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": instruction,
                }
            ],
        )

        # Ensure we have a valid response before accessing content
        if message.content and message.content[0].text:
            return message.content[0].text

        raise ValueError("Received an empty response from Anthropic API.")
