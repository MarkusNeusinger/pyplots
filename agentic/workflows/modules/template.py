"""Shared template loading and rendering for workflow scripts."""

import os


def load_template(template_path: str, working_dir: str) -> str:
    """Load a template file from the working directory."""
    full_path = os.path.join(working_dir, template_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Template not found: {full_path}")
    with open(full_path, "r") as f:
        return f.read()


def render_template(template: str, variables: dict) -> str:
    """Render a template by replacing $1, $2, $ARGUMENTS variables."""
    result = template
    for key, value in variables.items():
        if key.isdigit():
            result = result.replace(f"${key}", str(value))
    if "ARGUMENTS" in variables:
        result = result.replace("$ARGUMENTS", str(variables["ARGUMENTS"]))
    return result
