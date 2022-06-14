"""OSR console application."""

import argparse

from osr_mechanical import __version__


def main() -> int:
    """OSR console application."""
    parser = argparse.ArgumentParser(description="OSR console.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.parse_args()

    parser.print_help()
    exit(1)


if __name__ == "__main__":
    main()
