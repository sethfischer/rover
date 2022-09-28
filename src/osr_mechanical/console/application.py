"""OSR console command."""

import argparse
import base64
import datetime
import logging
from os import EX_OK, getcwd
from pathlib import Path
from shutil import rmtree
from sys import stdout

from cadquery import exporters
from invoke import run
from jinja2 import Environment, PackageLoader, select_autoescape

from osr_mechanical import __version__
from osr_mechanical.config import (
    COPYRIGHT_OWNER,
    DOCUMENTATION_URL,
    PROJECT_HOST,
    PROJECT_NAME,
    PROJECT_URL,
    REPO_URL,
    SHORT_DESCRIPTION,
)
from osr_mechanical.console.dxf import dxf_import_export
from osr_mechanical.console.exporters import ExportPNG
from osr_mechanical.final import FinalAssembly
from osr_mechanical.jigs.vslot import EndTapJig


def get_logger(name: str) -> logging.Logger:
    """Configure logger."""
    logger = logging.getLogger(name)
    logger.handlers.clear()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    )
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    return logger


logger = get_logger(__name__)


def export_png_cmd(args: argparse.Namespace) -> None:
    """Export PNG image of final assembly."""
    logger.debug("Exporting final assembly PNG.")

    out_file = args.out_file[0]
    label = args.no_label

    exporter = ExportPNG(out_file, height=args.height, width=args.width, label=label)
    exporter.export()

    exit(EX_OK)


def create_open_graph_card_svg(args: argparse.Namespace) -> None:
    """Create Open Graph Card in SVG format."""
    env = Environment(
        loader=PackageLoader("osr_mechanical"), autoescape=select_autoescape()
    )

    logo_cq = env.get_template("open-graph-card/logo-cadquery.svg").render()
    logo_cq_64 = base64.b64encode(logo_cq.encode("ascii")).decode("ascii")

    logo_ros = env.get_template("open-graph-card/logo-ros.svg").render()
    logo_ros_64 = base64.b64encode(logo_ros.encode("ascii")).decode("ascii")

    logo_python = env.get_template("open-graph-card/logo-python.svg").render()
    logo_python_64 = base64.b64encode(logo_python.encode("ascii")).decode("ascii")

    logo_github = env.get_template("open-graph-card/logo-github.svg").render()
    logo_github_64 = base64.b64encode(logo_github.encode("ascii")).decode("ascii")

    build_time = datetime.date.today()

    template = env.get_template("open-graph-card/open-graph-card.svg")
    result = template.render(
        build_time=build_time,
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


def get_release_dir() -> Path:
    """Release directory name."""
    return Path(f"sethfischer-osr-cam-{__version__}")


def export_jigs(out_directory: Path) -> None:
    """Export jigs as STL for 3D printing."""
    logger.debug("Exporting jigs.")

    out_directory.mkdir()

    end_tap_jig_pathname = out_directory / "vslot-end-tap-jig-2020.stl"
    end_tap_jig = EndTapJig(simple=True)
    exporters.export(end_tap_jig.cq_part("body"), str(end_tap_jig_pathname))


def export_final_assembly_step(out_file: Path) -> None:
    """Export final assembly as STEP."""
    logger.debug("Exporting final assembly STEP.")

    exporters.export(
        FinalAssembly().cq_object.toCompound(),
        str(out_file),
        tolerance=0.01,
        angularTolerance=0.1,
    )


def export_final_assembly_png(out_file: Path) -> None:
    """Export PNG image of final assembly for release archive."""
    logger.debug("Exporting final assembly PNG of release archive.")

    exporter = ExportPNG(out_file)
    exporter.export()


def create_readme(out_file: Path) -> int:
    """Create readme file."""
    logger.debug("Creating readme file.")

    env = Environment(
        loader=PackageLoader("osr_mechanical"), autoescape=select_autoescape()
    )

    build_time = datetime.date.today()

    template = env.get_template("README.md")
    result = template.render(
        build_time=build_time,
        copyright_owner=COPYRIGHT_OWNER,
        documentation_url=DOCUMENTATION_URL,
        project_repo_url=REPO_URL,
        project_url=PROJECT_URL,
        short_description=SHORT_DESCRIPTION,
        version=__version__,
    )

    return out_file.write_text(result)


def export_changelog(out_file: Path) -> int:
    """Export changelog."""
    logger.debug("Exporting changelog.")

    result = run(f"cz changelog --file-name {out_file}")

    return result.return_code


def build_cam_archive(args: argparse.Namespace) -> None:
    """Build Computer Aided Manufacturing file archive."""
    if not args.build_dir.is_dir():
        logger.critical(f"Build directory does not exist {args.build_dir}.")
        exit(1)

    release_dir = args.build_dir / get_release_dir()

    if release_dir.is_dir():
        logger.info(f"Removing release directory {release_dir}.")
        rmtree(release_dir)

    release_dir.mkdir()

    create_readme(release_dir / "README.md")
    export_changelog(release_dir / "CHANGELOG.md")
    export_final_assembly_step(release_dir / "sethfischer-osr.step")
    export_final_assembly_png(release_dir / "sethfischer-osr.png")
    export_jigs(release_dir / "jigs")

    exit(EX_OK)


def dxf_reduce(args: argparse.Namespace) -> None:
    """Import a DXF followed by export."""
    output = dxf_import_export(args.filename)
    stdout.write(output)
    exit(1)


def build_parser() -> argparse.ArgumentParser:
    """Parse arguments."""
    parser = argparse.ArgumentParser(prog="console", description="OSR console command.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
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
    parser_export_png.set_defaults(func=export_png_cmd)

    parser_open_graph_card = subparsers.add_parser(
        "open-graph-card",
        help="create open graph card SVG",
    )
    parser_open_graph_card.set_defaults(func=create_open_graph_card_svg)

    return parser


def main() -> int:
    """OSR console command."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("Too few arguments.")

    func(args)  # noqa

    return 1


if __name__ == "__main__":
    main()
