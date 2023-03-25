"""Sphinx configuration."""

from datetime import date

import sphinx_rtd_theme  # type: ignore[import] # noqa: F401

project = "sethfischer-osr"
release = "0.1.0"
author = "Seth Fischer"
project_copyright = f"{date.today().year}, {author}"


exclude_patterns = ["_build"]
extensions = [
    "osr_sphinx",
    "sphinx_argparse_cli",
    "sphinx_design",
    "sphinx_rtd_theme",
    "sphinxcontrib.cadquery",
]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


cadquery_include_source = False
