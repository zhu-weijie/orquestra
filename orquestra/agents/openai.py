from openai import OpenAI

from orquestra.models import Agent

from .base import BaseAgentExecutor


class OpenAIAgentExecutor(BaseAgentExecutor):
    """An agent executor for OpenAI models."""

    def __init__(self):
        # The client will automatically look for the OPENAI_API_KEY
        # environment variable.
        self.client = OpenAI()

    def execute(self, agent: Agent, instruction: str) -> str:
        """Executes a task using the OpenAI API."""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": instruction,
                }
            ],
            model=agent.model,
        )

        # Ensure we have a valid response before accessing content
        if chat_completion.choices and chat_completion.choices[0].message:
            return chat_completion.choices[0].message.content or ""

        raise ValueError("Received an empty response from OpenAI API.")
