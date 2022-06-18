"""OSR console application."""

import argparse
import logging
from os import EX_OK, getcwd
from pathlib import Path
from shutil import rmtree

from cadquery import exporters

from osr_mechanical import __version__
from osr_mechanical.jigs.vslot import EndTapJig

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)


def export_jigs(release_dir: Path):
    """Export jigs as STL for 3D printing."""
    logging.debug("Exporting jigs.")
    jig_dir = release_dir / "jigs"
    jig_dir.mkdir()

    end_tap_jig_pathname = jig_dir / "vslot-end-tap-jig-2020.stl"
    result = EndTapJig().make()
    exporters.export(result, str(end_tap_jig_pathname))


def get_release_dir() -> Path:
    """Release directory name."""
    return Path(f"sethfischer-osr-{__version__}")


def build(args):
    """Build release assets."""
    if not args.build_dir.is_dir():
        logging.critical(f"Build directory does not exist {args.build_dir}.")
        exit(1)

    release_dir = args.build_dir / get_release_dir()

    if release_dir.is_dir():
        logging.info(f"Removing release directory {release_dir}.")
        rmtree(release_dir)

    release_dir.mkdir()
    export_jigs(release_dir)

    exit(EX_OK)


def main() -> int:
    """OSR console application."""
    parser = argparse.ArgumentParser(description="OSR console.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers()

    parser_build = subparsers.add_parser("build", help="build release assets")
    parser_build.add_argument(
        "--build-dir",
        type=Path,
        default=Path(getcwd()).absolute() / "_build",
        help="build directory",
    )
    parser_build.set_defaults(func=build)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        logging.error("Invalid arguments.")

    parser.print_help()

    return 1


if __name__ == "__main__":
    main()
