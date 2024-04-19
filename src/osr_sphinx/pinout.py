"""Pinout Sphinx directives.

Sphinx directives for generating pinout diagrams using
`j0ono0/pinout <https://github.com/j0ono0/pinout/>`__.
"""

import hashlib
import shutil
import tempfile
from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

from docutils import nodes
from pinout.manager import export_diagram
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from osr_sphinx.utilities.utils import relative_uri


def sha1_file_contents(path: Path) -> Any:
    """Calculate the SHA1 hash of a file."""
    buffer_size = 65536
    sha1 = hashlib.sha1()

    with open(path.as_posix(), "rb") as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            sha1.update(data)

    return sha1


def set_pinout_image_uri(app: Sphinx, doctree: Any) -> None:
    """Export pinout diagrams.

    To be called on the Sphinx doctree-read event.
    """
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, "pinout"):
            continue

        diagram_id = img.pinout["diagram_id"]

        with as_file(
            files(f"osr_elec.pinout.{diagram_id}").joinpath("diagram.py")
        ) as src:
            with tempfile.TemporaryDirectory() as tmp_dir_name:
                tmp_dest = Path(tmp_dir_name) / "diagram.svg"

                export_diagram(src, tmp_dest, instance_name="diagram", overwrite=True)
                sha1 = sha1_file_contents(tmp_dest)

                dest = (
                    Path(app.builder.outdir)
                    .joinpath("_static")
                    .joinpath("pinout")
                    .joinpath(f"{diagram_id}-{sha1.hexdigest()}.svg")
                )

                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(tmp_dest, dest)

                img["uri"] = relative_uri(app, dest).as_posix()


class Pinout(SphinxDirective):
    """Pinout Sphinx directive.

    Generate a pinout diagram.
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0

    def run(self) -> list[nodes.Node]:
        """Insert pinout diagram as figure element with caption."""
        figure_node = nodes.figure()
        self.add_name(figure_node)

        image_node = nodes.image(
            "source", alt="alt", uri="data:image/svg+xml;base64,placeholder"
        )
        image_node.pinout = {  # type: ignore[attr-defined]
            "diagram_id": self.arguments[0],
        }
        figure_node += image_node

        node = nodes.Element()  # anonymous container for parsing content
        self.state.nested_parse(self.content, self.content_offset, node)
        caption_node = node[0]
        caption = nodes.caption(
            caption_node.rawsource,  # type: ignore[attr-defined]
            "",
            *caption_node.children,
        )
        figure_node += caption

        return [figure_node]
