"""Commitizen Sphinx directives."""

import subprocess

from docutils import nodes
from docutils.frontend import OptionParser
from docutils.utils import new_document
from sphinx.parsers import RSTParser
from sphinx.util.docutils import SphinxDirective


class CzChangelog(SphinxDirective):
    """Commitizen changelog Sphinx directive.

    Generate a changelog using the
    `Commitizen <https://commitizen-tools.github.io/commitizen/>`__
    command ``cz changelog``.
    """

    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self) -> list[nodes.Node]:
        """Run Commitizen changelog."""
        changelog = self.get_changelog()

        return self.parse_rst(changelog)

    @staticmethod
    def get_changelog() -> str:
        """Execute cz changelog and capture output."""
        result = subprocess.run(
            ["cz", "changelog", "--dry-run", "--file-name", "CHANGELOG.rst"],
            stdout=subprocess.PIPE,
        )

        return result.stdout.decode("utf-8")

    def parse_rst(self, text: str) -> list[nodes.Node]:
        """Parse reStructuredText string."""
        parser = RSTParser()
        parser.set_application(self.env.app)
        settings = OptionParser(
            defaults=self.env.settings,
            components=(RSTParser,),
            read_config_files=True,
        ).get_default_values()

        document = new_document("<rst-doc>", settings=settings)
        parser.parse(text, document)

        return document.children
