"""CadQuery wrappers."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any, Optional

import cadquery.occ_impl.exporters
from cadquery import Shape, Workplane
from cadquery.occ_impl.exporters import ExportLiterals
from wurlitzer import STDOUT, pipes


class Export:
    """Wrapper for cadquery.occ_impl.exporters.export.

    Some OCCT export methods write undesired output directly to stdout from the C code,
    meaning ``contextlib.redirect_stdout`` is not effective.

    See:

    * https://docs.python.org/3/library/contextlib.html
    * https://bugs.python.org/issue24500
    """

    _stdout: str

    def __init__(self) -> None:
        """Initialise."""
        self._stdout = ""

    @property
    def stdout(self) -> str:
        """Output sent to stdout."""
        return self._stdout

    def export(
        self,
        w: Shape | Workplane,
        fname: Path,
        export_type: Optional[ExportLiterals] = None,
        tolerance: float = 0.1,
        angular_tolerance: float = 0.1,
        opt: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Export Workplane or Shape to file. Multiple entities are converted to compound.

        :param w: Shape or Workplane to be exported.
        :param fname: output filename.
        :param export_type: the exportFormat to use. If None will be inferred from the
            extension. Default: None.
        :param tolerance: the deflection tolerance, in model units. Default 0.1.
        :param angular_tolerance: the angular tolerance, in radians. Default 0.1.
        :param opt: additional options passed to the specific exporter. Default None.
        """
        export_stdout = StringIO()

        with pipes(stdout=export_stdout, stderr=STDOUT):
            result = cadquery.occ_impl.exporters.export(
                w,
                str(fname),
                export_type,
                tolerance,
                angular_tolerance,
                opt,
            )

        self._stdout = export_stdout.getvalue()

        return result
