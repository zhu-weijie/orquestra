from typing import Any, Dict

from jinja2 import Environment, StrictUndefined


def render_template(template_str: str, context: Dict[str, Any]) -> str:
    """
    Renders a Jinja2 template string with the given context.

    Args:
        template_str: The string containing Jinja2 template variables.
        context: A dictionary of values to render the template with.

    Returns:
        The rendered string.

    Raises:
        jinja2.exceptions.UndefinedError: If a variable in the template
                                          is not found in the context.
    """
    # Using StrictUndefined makes rendering fail on missing variables,
    # which is safer for our use case.
    env = Environment(undefined=StrictUndefined)
    template = env.from_string(template_str)
    return template.render(context)
