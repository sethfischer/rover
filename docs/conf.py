import sphinx_rtd_theme
from datetime import date


project = "sethfischer/osr"
release = "0.1.0-pre-alpha"
author = "Seth Fischer"
copyright = f"{date.today().year}, {author}"


exclude_patterns = ["_build"]
extensions = [
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
