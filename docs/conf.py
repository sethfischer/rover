"""Sphinx configuration."""

from datetime import date

import sphinx_rtd_theme  # type: ignore[import] # noqa: F401

project = "sethfischer-osr"
release = "0.1.0"
author = "Seth Fischer"
copyright = f"{date.today().year}, {author}"


exclude_patterns = ["_build"]
extensions = [
    "sphinx_argparse_cli",
    "sphinx_lfs_content",
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
