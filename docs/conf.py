"""Sphinx configuration."""

from datetime import date

import sphinx_rtd_theme  # type: ignore[import] # noqa: F401

project = "sethfischer-rover"
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
templates_path = [
    "_templates",
]


html_context = {
    "display_star_on_github": True,
}
html_favicon = "_static/images/icon.svg"
html_static_path = ["_static"]
html_theme = "sphinx_rtd_theme"


cadquery_include_source = False
