"""OSR Sphinx extension."""

from typing import Any

import sphinx.application

from osr_mechanical import __version__
from osr_sphinx.bom import BomTable
from osr_sphinx.print_settings import PrinterSettings


def setup(app: sphinx.application.Sphinx) -> dict[str, Any]:
    """Set up."""
    app.add_directive("osr-bom", BomTable)
    app.add_directive("osr-print-settings", PrinterSettings)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
