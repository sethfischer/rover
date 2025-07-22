"""Sphinx osr (rover.fischer.nz) domain."""

from typing import AbstractSet, Any

from docutils.nodes import Element, reference
from sphinx.addnodes import pending_xref
from sphinx.builders import Builder
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment

from osr_sphinx.bom import BomTable
from osr_sphinx.commitizen import CzChangelog
from osr_sphinx.dimensions import DimensionRole
from osr_sphinx.pinout import Pinout
from osr_sphinx.print_settings import PrintSettings


class OsrDomain(Domain):
    """OSR domain."""

    name = "osr"
    label = "Open Source Rover"

    directives = {
        "bom": BomTable,
        "cz-changelog": CzChangelog,
        "pinout-diagram": Pinout,
        "print-settings": PrintSettings,
    }
    roles = {
        "dimension": DimensionRole(),
    }

    def merge_domaindata(
        self, docnames: AbstractSet[str], otherdata: dict[str, Any]
    ) -> None:
        """Merge in data regarding docnames from a different domaindata inventory."""
        pass

    def resolve_any_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> list[tuple[str, reference]]:
        """Resolve the pending_xref node with the given target."""
        return []
