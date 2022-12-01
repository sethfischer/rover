"""DXF utilities."""


import tempfile
from pathlib import Path

from cadquery import exporters, importers


def dxf_import_export(filepath: Path) -> str:
    """Import then export a DXF.

    This can result in a reduced file size. But in no way is it a lossless conversion.
    """
    result = importers.importDXF(filepath)  # type: ignore[no-untyped-call]

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / filepath.name
        exporters.export(result, str(tmp_file), "DXF")
        output = tmp_file.read_text()

    return output
