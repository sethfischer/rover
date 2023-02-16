"""Calculate dimensions of CadQuery model."""

from docutils import nodes
from sphinx.util import logging
from sphinx.util.docutils import SphinxRole

from osr_sphinx.utilities.final_assembly import final_assembly

logger = logging.getLogger(__name__)


class DimensionRole(SphinxRole):
    """Role to calculate bounding box dimensions."""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Run the role."""
        _valid_labels = {"height", "width", "length"}

        if self.text not in _valid_labels:
            msg = self.inliner.reporter.error(  # type: ignore[attr-defined]
                (
                    f"Invalid dimension label: {self.text}. "
                    f"Expected one of {', '.join(str(s) for s in _valid_labels)}."
                ),
                line=self.lineno,
            )
            prb = self.inliner.problematic(  # type: ignore[attr-defined]
                self.rawtext,
                self.rawtext,
                msg,
            )
            return [prb], [msg]

        value_formatted = self._get_value(self.text)

        node = nodes.raw("", nodes.Text(value_formatted), format="html")
        self.set_source_info(node)
        return [node], []

    @staticmethod
    def _get_value(label: str) -> str:
        """Get dimensional value and format."""
        assembly = final_assembly.cq_object.toCompound()
        bounding_box = assembly.BoundingBox()

        value = float(0)

        if "height" == label:
            value = bounding_box.zlen
        elif "width" == label:
            value = bounding_box.xlen
        elif "length" == label:
            value = bounding_box.ylen

        return f"{value:.0f} mm"
