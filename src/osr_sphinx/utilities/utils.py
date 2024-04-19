"""General utilities for Sphinx extensions."""

from pathlib import Path

from sphinx.application import Sphinx


def relative_uri(app: Sphinx, asset: Path) -> Path:
    """Return the URI of an asset relative to the current document."""
    doc_name_absolute = Path(app.srcdir) / Path(app.builder.env.docname)
    doc_depth = len(doc_name_absolute.parent.relative_to(app.srcdir).parts)

    relative_to_document_part = Path("../" * doc_depth)
    uri = relative_to_document_part / asset.relative_to(Path(app.builder.outdir))

    return uri
