from pathlib import Path

import yaml

from orquestra.models import Workflow


def parse_workflow_from_yaml(file_path: Path) -> Workflow:
    """
    Parses a YAML file and validates it against the Workflow model.

    Args:
        file_path: The path to the YAML file.

    Returns:
        A validated Workflow object.
    """
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    # Pydantic's `model_validate` will parse the dict and raise
    # a ValidationError if the data is invalid.
    return Workflow.model_validate(data)
