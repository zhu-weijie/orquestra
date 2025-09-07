from typing import Any, Dict

from orquestra.models import Workflow

from .scheduler import resolve_task_order
from .templating import render_template


class Orchestrator:
    """
    Manages the execution of a workflow.
    """

    def __init__(self, workflow: Workflow):
        self.workflow = workflow
        # Simple context to store task outputs
        self.context: Dict[str, Any] = {"tasks": {}}

    def run(self) -> Dict[str, Any]:
        """
        Executes the workflow in a simulated (dry-run) mode.

        Returns:
            The final context dictionary with all task results.
        """
        execution_plan = resolve_task_order(self.workflow.tasks)

        print(f"\nExecuting workflow: '{self.workflow.name}'")
        for i, batch in enumerate(execution_plan):
            print(
                f"--> Running Batch {i+1} with {len(batch)} task(s): {[t.name for t in batch]}"
            )
            for task in batch:
                # 1. Render the instruction template
                rendered_instruction = render_template(task.instruction, self.context)
                print(f"    - Executing task '{task.name}'...")
                print(f"      Instruction: {rendered_instruction}")

                # 2. Simulate execution (replace with actual agent call later)
                # For now, we just create a placeholder output
                task_output = f"Simulated output from task '{task.name}'"

                # 3. Update the context with the result
                if task.name not in self.context["tasks"]:
                    self.context["tasks"][task.name] = {}

                self.context["tasks"][task.name]["output"] = task_output

        print("Workflow execution finished.")
        return self.context
