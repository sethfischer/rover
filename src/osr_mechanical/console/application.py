"""OSR console command."""

import csv
import importlib
import logging
import tarfile
from argparse import ArgumentParser, Namespace
from base64 import b64encode
from datetime import datetime
from json import JSONDecodeError
from os import EX_OK, getcwd
from pathlib import Path
from shutil import rmtree
from subprocess import run
from sys import stdout
from zipfile import ZIP_DEFLATED, ZipFile

from cadquery import exporters
from jinja2 import Environment, PackageLoader, select_autoescape

from osr_mechanical import __version__
from osr_mechanical.bom.bom import Bom
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

logging.basicConfig(encoding="utf-8", level=logging.INFO)
logger = logging.getLogger("osr_mechanical.console")


def export_png_cmd(args: Namespace) -> None:
    """Export PNG image of final assembly."""
    logger.debug("Exporting final assembly PNG.")

    out_file = args.out_file[0]
    label = args.no_label

    exporter = ExportPNG(out_file, height=args.height, width=args.width, label=label)
    exporter.export()

    exit(EX_OK)


def create_open_graph_card_svg(args: Namespace) -> None:
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


def get_release_name(project_name: str, version: str) -> str:
    """Release name."""
    return f"{project_name}-cam-{version}"


def export_jigs(out_directory: Path) -> None:
    """Export jigs as STL for 3D printing."""
    logger.debug("Exporting jigs.")

    out_directory.mkdir()

    end_tap_jig_pathname = out_directory / "vslot-end-tap-jig-2020.stl"
    end_tap_jig = EndTapJig(simple=True)
    exporters.export(
        end_tap_jig.cq_part("2020_end_tap_jig__body"),
        str(end_tap_jig_pathname),
    )


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

    now = datetime.utcnow()

    template = env.get_template("README.md")
    result = template.render(
        build_time=now,
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

    result = run(
        ["cz", "changelog", "--file-name", out_file],
        capture_output=True,
        text=True,
    )
    result.check_returncode()

    return result.returncode


def tar_directory(directory: Path, out_file: Path, arcname: str):
    """Create tar archive of a directory."""
    logger.debug(f"Creating tar archive {out_file}.")
    with tarfile.open(out_file, "w:gz") as tar:
        tar.add(directory, arcname=arcname)


def zip_directory(directory: Path, out_file: Path, arcname: str):
    """Create zip archive of directory."""
    logger.debug(f"Creating zip archive {out_file}.")
    with ZipFile(out_file, "w", ZIP_DEFLATED) as zip_file:
        for entry in directory.rglob("*"):
            zip_file.write(entry, Path(arcname / entry.relative_to(directory)))


def build_cam_archive(args: Namespace) -> None:
    """Build Computer Aided Manufacturing file archive."""
    if not args.build_dir.is_dir():
        logger.critical(f"Build directory does not exist {args.build_dir}.")
        exit(1)

    release_name = get_release_name(PROJECT_NAME, __version__)
    release_directory = args.build_dir / release_name

    if release_directory.is_dir():
        logger.info(f"Removing release directory {release_directory}.")
        rmtree(release_directory)

    release_directory.mkdir()

    create_readme(release_directory / "README.md")
    export_changelog(release_directory / "CHANGELOG.md")
    export_final_assembly_step(release_directory / f"{PROJECT_NAME}.step")
    export_final_assembly_png(release_directory / f"{PROJECT_NAME}.png")
    export_jigs(release_directory / "jigs")
    export_bom(release_directory / "bom")

    tar_directory(
        release_directory,
        args.build_dir / f"{release_name}.tar.gz",
        release_name,
    )

    zip_directory(
        release_directory,
        args.build_dir / f"{release_name}.zip",
        release_name,
    )

    exit(EX_OK)


def dxf_reduce(args: Namespace) -> None:
    """Import a DXF followed by export."""
    output = dxf_import_export(args.filename)
    stdout.write(output)
    exit(1)


def export_bom(out_directory: Path) -> None:
    """Export bill of materials."""
    logger.debug("Exporting bill of materials.")

    out_directory.mkdir()
    csv_pathname = out_directory / "bom.csv"

    final = FinalAssembly()
    jig_end_tap = EndTapJig()

    bom = Bom()
    bom.insert_assembly(final.cq_object)
    bom.insert_assembly(jig_end_tap.cq_object)

    data = bom.encode(encoder=Bom.ENCODE_CSV)

    with open(csv_pathname, mode="w") as f:
        f.write(data)


def generate_bom(args: Namespace) -> None:
    """Generate bill of materials."""
    module_name, class_name = f"osr_mechanical.{args.assembly}".rsplit(".", 1)

    try:
        module = importlib.import_module(module_name)
        assembly_container = getattr(module, class_name)

        assembly = assembly_container().cq_object
        bom = Bom(assembly)

        stdout.write(bom.encode(encoder=args.encode) + "\n")
        exit(EX_OK)
    except AttributeError:
        logger.error(f"Class {class_name} does not exist.")
    except ImportError:
        logger.error(f"Module {module_name} does not exist.")
    except csv.Error as error:
        logger.error(f"CSV encoding error: {error}.")
    except JSONDecodeError as error:
        logger.error(f"JSON encoding error: {error}.")

    exit(1)


def build_parser() -> ArgumentParser:
    """Parse arguments."""
    parser = ArgumentParser(prog="console", description="OSR console command.")
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
    parser_export_png.set_defaults(func=export_png_cmd)

    parser_open_graph_card = subparsers.add_parser(
        "open-graph-card",
        help="create open graph card SVG",
    )
    parser_open_graph_card.set_defaults(func=create_open_graph_card_svg)

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
    parser_bom.set_defaults(func=generate_bom)

    return parser


def main() -> int:
    """OSR console command."""
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
