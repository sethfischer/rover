"""Rover console command."""

import importlib
import logging
import tempfile
from argparse import ArgumentParser, Namespace
from base64 import b64encode
from datetime import datetime
from os import EX_OK, getcwd
from pathlib import Path
from sys import stdout

from cadquery import exporters as cq_exporters
from jinja2 import Environment, PackageLoader, select_autoescape

from osr_mechanical import __version__
from osr_mechanical.bom.bom import Bom, BomBuilder
from osr_mechanical.config import (
    COPYRIGHT_OWNER,
    PROJECT_HOST,
    PROJECT_NAME,
    SHORT_DESCRIPTION,
)
from osr_mechanical.console.dxf import dxf_import_export
from osr_mechanical.console.exporters import ExportPNG
from osr_mechanical.console.release import ReleaseBuilder
from osr_mechanical.console.utilities import snake_to_camel_case

logging.basicConfig(encoding="utf-8", level=logging.INFO)
logger = logging.getLogger("osr_mechanical.console")


def export_png(args: Namespace) -> None:
    """Export PNG image of final assembly."""
    logger.debug("Exporting final assembly PNG.")

    out_file = args.out_file[0]
    label = args.no_label

    exporter = ExportPNG(out_file, height=args.height, width=args.width, label=label)
    exporter.export()

    exit(EX_OK)


def open_graph_card_svg(_args: Namespace) -> None:
    """Create Open Graph Card in SVG format."""
    env = Environment(
        loader=PackageLoader("osr_mechanical"), autoescape=select_autoescape()
    )

    logo_cq = env.get_template("open-graph-card/logo-cadquery.svg").render()
    logo_cq_64 = b64encode(logo_cq.encode("ascii")).decode("ascii")

    logo_ros = env.get_template("open-graph-card/logo-ros.svg").render()
    logo_ros_64 = b64encode(logo_ros.encode("ascii")).decode("ascii")

    logo_python = env.get_template("open-graph-card/logo-python.svg").render()
    logo_python_64 = b64encode(logo_python.encode("ascii")).decode("ascii")

    logo_github = env.get_template("open-graph-card/logo-github.svg").render()
    logo_github_64 = b64encode(logo_github.encode("ascii")).decode("ascii")

    now = datetime.utcnow()

    template = env.get_template("open-graph-card/open-graph-card.svg")
    result = template.render(
        build_time=now,
        copyright_owner=COPYRIGHT_OWNER,
        cq_logo=logo_cq_64,
        github_logo=logo_github_64,
        project_host=PROJECT_HOST,
        project_name=PROJECT_NAME,
        python_logo=logo_python_64,
        ros_logo=logo_ros_64,
        short_description=SHORT_DESCRIPTION,
    )

    stdout.write(result)

    exit(EX_OK)


def build_cam_archive(args: Namespace) -> None:
    """Build Computer Aided Manufacturing file archive."""
    if not args.build_dir.is_dir():
        logger.critical(f"Build directory does not exist {args.build_dir}.")
        exit(1)

    builder = ReleaseBuilder(args.build_dir)
    builder.build()

    exit(EX_OK)


def dxf_reduce(args: Namespace) -> None:
    """Import a DXF followed by export."""
    output = dxf_import_export(args.filename)
    stdout.write(output)
    exit(EX_OK)


def export_bom(args: Namespace) -> None:
    """Generate bill of materials."""
    builder = BomBuilder()
    bom = builder.from_string(args.assembly)

    stdout.write(bom.encode(encoder=args.encode) + "\n")
    exit(EX_OK)


def export_pcb_outline(args: Namespace) -> None:
    """Export PCB outlines as DXF."""
    module_name = (
        f"osr_mechanical.pcb.{args.board}.{snake_to_camel_case(args.board)}Board"
    )

    module_name, class_name = module_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    container = getattr(module, class_name)

    pcb_face = container(mounting_holes=False, full_size=True).board_face()

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / "tmp.dxf"
        cq_exporters.export(pcb_face, str(tmp_file), "DXF")

        stdout.write(tmp_file.read_text())

    exit(EX_OK)


def build_parser() -> ArgumentParser:
    """Parse arguments."""
    parser = ArgumentParser(prog="console", description="Rover console command.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--debug",
        help="Set log level to DEBUG",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        default=logging.WARNING,
    )
    parser.add_argument(
        "--verbose",
        help="Set log level to INFO",
        action="store_const",
        dest="log_level",
        const=logging.INFO,
    )

    subparsers = parser.add_subparsers()

    parser_build = subparsers.add_parser(
        "build", help="create files for computer-aided manufacturing (e.g. STL)"
    )
    parser_build.add_argument(
        "--build-dir",
        type=Path,
        default=Path(getcwd()).absolute() / "_build",
        help="build directory",
    )
    parser_build.set_defaults(func=build_cam_archive)

    parser_dxf_reduce = subparsers.add_parser(
        "dxf-reduce",
        help="reduce the size of a DXF file",
        epilog=(
            "Warning: This can result in a reduced file size. "
            "But in no way is it a lossless conversion."
        ),
    )
    parser_dxf_reduce.add_argument(
        "filename",
        type=Path,
        help="input DXF file",
    )
    parser_dxf_reduce.set_defaults(func=dxf_reduce)

    parser_export_png = subparsers.add_parser(
        "export-png",
        help="export PNG image of final assembly",
    )
    parser_export_png.add_argument(
        "--width",
        type=int,
        default=1000,
        help="width of image in pixels",
    )
    parser_export_png.add_argument(
        "--height",
        type=int,
        default=750,
        help="height of image in pixels",
    )
    parser_export_png.add_argument(
        "--no-label",
        action="store_false",
        help="do not label image",
    )
    parser_export_png.add_argument(
        "out_file",
        type=Path,
        nargs=1,
        help="output file",
    )
    parser_export_png.set_defaults(func=export_png)

    parser_open_graph_card = subparsers.add_parser(
        "open-graph-card",
        help="create open graph card SVG",
    )
    parser_open_graph_card.set_defaults(func=open_graph_card_svg)

    parser_bom = subparsers.add_parser("bom", help="generate bill of materials")
    parser_bom.add_argument(
        "--encode",
        type=str,
        default=Bom.ENCODE_JSON,
        help="output format",
    )
    parser_bom.add_argument(
        "--assembly",
        type=str,
        default="final.FinalAssembly",
        help="assembly for which to generate bill of materials",
    )
    parser_bom.set_defaults(func=export_bom)

    parser_pcb_outline = subparsers.add_parser(
        "pcb-outline", help="generate printed circuit board outlines"
    )
    parser_pcb_outline.add_argument(
        "--board",
        required=True,
        type=str,
        help="board for which to generate outline",
    )
    parser_pcb_outline.set_defaults(func=export_pcb_outline)

    return parser


def main() -> int:
    """Rover console command."""
    parser = build_parser()
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)

    try:
        func = args.func
    except AttributeError:
        parser.error("Too few arguments.")

    func(args)  # noqa

    return 1


if __name__ == "__main__":
    main()
