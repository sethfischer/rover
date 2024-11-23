"""Singleton for creating a CadQuery model of the final assembly."""

from sphinx.util import logging
from sphinx.util.console import bold

from osr_mechanical.final import FinalAssembly

logger = logging.getLogger(__name__)
logger.info(bold("creating CadQuery model of final assembly... "), nonl=True)

final_assembly = FinalAssembly(simple=True)

logger.info("done")
