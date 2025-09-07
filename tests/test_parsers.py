from pathlib import Path

from orquestra.parsers import parse_workflow_from_yaml


def test_parse_valid_yaml_workflow():
    """
    Tests that a valid YAML workflow file is parsed correctly.
    """
    # Get the path to the example file
    example_file = Path(__file__).parent.parent / "examples" / "simple_workflow.yaml"

    # Ensure the file exists before parsing
    assert example_file.exists(), "Example workflow file not found!"

    # Parse the workflow
    workflow = parse_workflow_from_yaml(example_file)

    # Assertions to verify the content
    assert workflow.name == "Simple Blog Post Workflow"
    assert len(workflow.agents) == 2
    assert workflow.agents[0].name == "writer_agent"
    assert len(workflow.tasks) == 2
    assert workflow.tasks[1].name == "edit_post"
    assert workflow.tasks[1].depends_on == ["draft_post"]
    print("\nYAML parser test passed successfully!")
