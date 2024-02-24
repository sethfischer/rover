"""Utilities."""


def snake_to_camel_case(snake_str: str) -> str:
    """Convert a snake case string to camel case."""
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))
