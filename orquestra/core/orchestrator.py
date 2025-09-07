from typing import Any, Dict, Type

from orquestra.agents.anthropic import AnthropicAgentExecutor
from orquestra.agents.base import BaseAgentExecutor
from orquestra.agents.openai import OpenAIAgentExecutor
from orquestra.models import Agent, Workflow

from .scheduler import resolve_task_order
from .templating import render_template


class Orchestrator:
    """
    Manages the execution of a workflow.
    """

    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        self.context: Dict[str, Any] = {"tasks": {}}

        # Registry of executor *classes*, not instances
        self.executor_classes: Dict[str, Type[BaseAgentExecutor]] = {
            "openai": OpenAIAgentExecutor,
            "anthropic": AnthropicAgentExecutor,
        }
        # Cache for instantiated executors (for lazy loading)
        self.executor_instances: Dict[str, BaseAgentExecutor] = {}

        self.agent_map: Dict[str, Agent] = {
            agent.name: agent for agent in self.workflow.agents
        }

    def _get_executor(self, agent: Agent) -> BaseAgentExecutor:
        """Finds or creates the appropriate executor for a given agent."""
        provider = agent.provider

        # Check if we already have an instance in our cache
        if provider in self.executor_instances:
            return self.executor_instances[provider]

        # If not, find the class and create a new instance
        executor_class = self.executor_classes.get(provider)
        if not executor_class:
            raise ValueError(f"No executor found for provider: {provider}")

        # Instantiate, cache it, and then return it
        instance = executor_class()
        self.executor_instances[provider] = instance
        return instance

    def run(self) -> Dict[str, Any]:
        execution_plan = resolve_task_order(self.workflow.tasks)

        print(f"\nExecuting workflow: '{self.workflow.name}'")
        for i, batch in enumerate(execution_plan):
            print(f"--> Running Batch {i+1}...")
            for task in batch:
                rendered_instruction = render_template(task.instruction, self.context)
                print(f"    - Executing task '{task.name}'...")

                # 1. Find the agent model and its executor
                agent_model = self.agent_map[task.agent]
                executor = self._get_executor(agent_model)

                # 2. Execute the task
                task_output = executor.execute(agent_model, rendered_instruction)

                # 3. Update context
                if task.name not in self.context["tasks"]:
                    self.context["tasks"][task.name] = {}
                self.context["tasks"][task.name]["output"] = task_output

        print("Workflow execution finished.")
        return self.context
