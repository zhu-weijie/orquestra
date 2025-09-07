import pytest
from jinja2.exceptions import UndefinedError

from orquestra.core import render_template


def test_simple_rendering():
    """Tests basic variable replacement."""
    template = "Hello, {{ name }}!"
    context = {"name": "Orquestra"}
    result = render_template(template, context)
    assert result == "Hello, Orquestra!"


def test_nested_data_rendering():
    """Tests accessing nested data within the context."""
    template = "The output of task A is: {{ tasks.task_a.output }}"
    context = {
        "tasks": {
            "task_a": {"output": "This is the result."},
            "task_b": {"output": "Some other result."},
        }
    }
    result = render_template(template, context)
    assert result == "The output of task A is: This is the result."


def test_rendering_with_no_variables():
    """Ensures a string without variables passes through unchanged."""
    template = "This is just a plain string."
    context = {"some_data": "value"}
    result = render_template(template, context)
    assert result == "This is just a plain string."


def test_missing_variable_raises_error():
    """
    Tests that rendering fails if a variable is not in the context,
    which prevents silent errors.
    """
    template = "Hello, {{ name }}!"
    context = {"wrong_key": "Orquestra"}
    with pytest.raises(UndefinedError, match="'name' is undefined"):
        render_template(template, context)
