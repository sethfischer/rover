"""Release builder."""

import tarfile
from datetime import datetime
from pathlib import Path
from shutil import rmtree
from subprocess import run
from zipfile import ZIP_DEFLATED, ZipFile

from cadquery import exporters
from jinja2 import Environment, PackageLoader, select_autoescape

from osr_mechanical import __version__
from osr_mechanical import __version__ as project_version
from osr_mechanical.bom.bom import Bom
from osr_mechanical.config import (
    COPYRIGHT_OWNER,
    DOCUMENTATION_URL,
    PROJECT_NAME,
    PROJECT_URL,
    REPO_URL,
    SHORT_DESCRIPTION,
)
from osr_mechanical.console.cq_wrappers import Export as ExportWrapper
from osr_mechanical.console.exporters import ExportPNG
from osr_mechanical.final import FinalAssembly
from osr_mechanical.jigs.vslot import EndTapJig


class ReleaseBuilder:
    """Build Computer Aided Manufacturing file archive."""

    def __init__(self, build_directory: Path):
        """Initialise ReleaseBuilder."""
        self.build_directory = build_directory
        self.release_name = f"{PROJECT_NAME}-cam-{project_version}"
        self.release_directory = self.build_directory / self.release_name

        if not self.build_directory.is_dir():
            raise FileNotFoundError(
                f"Build directory '{self.build_directory}' does not exist."
            )

    def build(self) -> None:
        """Build release."""
        self.remove_directory(self.release_directory)
        self.release_directory.mkdir()

        self.readme(self.release_directory / "README.md")
        self.changelog(self.release_directory / "CHANGELOG.md")
        self.final_assembly_step(self.release_directory / f"{PROJECT_NAME}.step")
        self.final_assembly_png(self.release_directory / f"{PROJECT_NAME}.png")
        self.jigs(self.release_directory / "jigs")
        self.bom(self.release_directory / "bom")
        self.archive()

    @staticmethod
    def remove_directory(release_directory: Path) -> None:
        """Remove release directory."""
        if release_directory.is_dir():
            rmtree(release_directory)

    @staticmethod
    def readme(out_file: Path) -> int:
        """Create README file."""
        env = Environment(
            loader=PackageLoader("osr_mechanical"),
            autoescape=select_autoescape(),
        )

        template = env.get_template("README.md")
        result = template.render(
            build_time=datetime.utcnow(),
            copyright_owner=COPYRIGHT_OWNER,
            documentation_url=DOCUMENTATION_URL,
            project_repo_url=REPO_URL,
            project_url=PROJECT_URL,
            short_description=SHORT_DESCRIPTION,
            version=__version__,
        )

        return out_file.write_text(result)

    @staticmethod
    def changelog(out_file: Path) -> int:
        """Create changelog."""
        result = run(
            ["cz", "changelog", "--file-name", out_file],
            capture_output=True,
            text=True,
        )
        result.check_returncode()

        return result.returncode

    @staticmethod
    def final_assembly_step(out_file: Path) -> None:
        """Export final assembly as STEP."""
        cq_object = FinalAssembly().cq_object.toCompound()

        export_wrapper = ExportWrapper()

        export_wrapper.export(
            cq_object,
            out_file,
            tolerance=0.01,
            angular_tolerance=0.1,
        )

    @staticmethod
    def final_assembly_png(out_file: Path) -> None:
        """Export PNG image of final assembly for release archive."""
        exporter = ExportPNG(out_file)
        exporter.export()

    @staticmethod
    def jigs(out_directory: Path) -> None:
        """Export jigs as STL for 3D printing."""
        out_directory.mkdir()

        end_tap_jig_pathname = out_directory / "vslot-end-tap-jig-2020.stl"
        end_tap_jig = EndTapJig(simple=True)
        exporters.export(
            end_tap_jig.cq_part("2020_end_tap_jig__body"),
            str(end_tap_jig_pathname),
        )

    @staticmethod
    def bom(out_directory: Path) -> None:
        """Export bill of materials."""
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

    def archive(self) -> None:
        """Create release archives."""
        self.tar(
            self.release_directory,
            self.build_directory / f"{self.release_name}.tar.gz",
            self.release_name,
        )

        self.zip(
            self.release_directory,
            self.build_directory / f"{self.release_name}.zip",
            self.release_name,
        )

    @staticmethod
    def tar(directory: Path, out_file: Path, arcname: str) -> None:
        """Create tar archive of release."""
        with tarfile.open(out_file, "w:gz") as tar:
            tar.add(directory, arcname=arcname)

    @staticmethod
    def zip(directory: Path, out_file: Path, arcname: str) -> None:
        """Create zip archive of release."""
        with ZipFile(out_file, "w", ZIP_DEFLATED) as zip_file:
            for entry in directory.rglob("*"):
                zip_file.write(entry, Path(arcname / entry.relative_to(directory)))
