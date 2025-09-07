from pathlib import Path

from orquestra.core import Orchestrator
from orquestra.parsers import parse_workflow_from_yaml


def test_orchestrator_dry_run():
    """
    Tests the full end-to-end dry run of the orchestrator,
    ensuring context is managed and templating works correctly.
    """
    # 1. Load the workflow
    workflow_path = Path(__file__).parent.parent / "examples" / "simple_workflow.yaml"
    workflow = parse_workflow_from_yaml(workflow_path)

    # 2. Instantiate and run the orchestrator
    orchestrator = Orchestrator(workflow)
    final_context = orchestrator.run()

    # 3. Assert the final state of the context
    assert "tasks" in final_context

    # Check the first task's result
    draft_task_result = final_context["tasks"]["draft_post"]
    assert "output" in draft_task_result
    assert draft_task_result["output"] == "Simulated output from task 'draft_post'"

    # Check the second task's result
    edit_task_result = final_context["tasks"]["edit_post"]
    assert "output" in edit_task_result
    assert edit_task_result["output"] == "Simulated output from task 'edit_post'"
