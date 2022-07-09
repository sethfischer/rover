"""OSR console command."""

import argparse
import logging
from os import EX_OK, getcwd
from pathlib import Path
from shutil import rmtree

from cadquery import exporters

from osr_mechanical import __version__
from osr_mechanical.jigs.vslot import EndTapJig


def get_logger(name: str):
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


def export_jigs(release_dir: Path):
    """Export jigs as STL for 3D printing."""
    logger.debug("Exporting jigs.")
    jig_dir = release_dir / "jigs"
    jig_dir.mkdir()

    end_tap_jig_pathname = jig_dir / "vslot-end-tap-jig-2020.stl"
    result = EndTapJig().make()
    exporters.export(result, str(end_tap_jig_pathname))


def get_release_dir() -> Path:
    """Release directory name."""
    return Path(f"sethfischer-osr-cam-{__version__}")


def build(args):
    """Build CAM file archive."""
    if not args.build_dir.is_dir():
        logger.critical(f"Build directory does not exist {args.build_dir}.")
        exit(1)

    release_dir = args.build_dir / get_release_dir()

    if release_dir.is_dir():
        logger.info(f"Removing release directory {release_dir}.")
        rmtree(release_dir)

    release_dir.mkdir()
    export_jigs(release_dir)

    exit(EX_OK)


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
    parser_build.set_defaults(func=build)

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
