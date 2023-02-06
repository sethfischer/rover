"""Custom exporters."""

from __future__ import annotations

from configparser import ConfigParser
from datetime import datetime
from math import ceil
from pathlib import Path
from subprocess import run
from tempfile import TemporaryDirectory
from typing import Any

from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from PIL.Image import Exif

from osr_common.cq_wrappers import Export as ExportWrapper
from osr_mechanical.config import (
    COPYRIGHT_NOTICE,
    COPYRIGHT_OWNER,
    LONG_DESCRIPTION,
    PROJECT_HOST,
    PROJECT_URL,
)
from osr_mechanical.final import FinalAssembly


class ExportPNG:
    """Export PNG raster image using Mayo.

    `Mayo <https://github.com/fougue/mayo>`_ 3D CAD viewer and converter based on Qt
    and OpenCascade.
    """

    EXIF_DATE_FORMAT = "%Y:%m:%d %H:%M:%S"

    def __init__(
        self,
        out_file: Path,
        width: int = 1000,
        height: int = 750,
        mayo_config: dict[str, Any] | None = None,
        label: bool = True,
    ) -> None:
        """Initialise ExportPNG."""
        self.out_file = out_file
        self.width = width
        self.height = height
        self.mayo_config = mayo_config
        self.label = label

        self.now = datetime.utcnow()
        self.font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

    def export(self) -> Path:
        """Export PNG image."""
        with TemporaryDirectory() as tmp_directory_name:
            tmp_directory = Path(tmp_directory_name)

            step_pathname = self.export_step(tmp_directory)

            mayo_config = self.create_mayo_config(
                self.height, self.width, self.mayo_config
            )
            mayo_config_pathname = Path(tmp_directory / "mayo.ini")
            with mayo_config_pathname.open("w") as file:
                mayo_config.write(file)

            exported_png = self.export_png(mayo_config_pathname, step_pathname)

            result_path = Path(tmp_directory / "result.png")
            image = Image.open(exported_png)

            if self.label:
                label = f"{PROJECT_HOST}    {self.now.strftime('%Y-%m-%d')}"
                image = self.label_image(image, label)

            exif = self.exif_tags()
            image.save(result_path, exif=exif)

            self.optimise_png(result_path)

            result_path.rename(self.out_file)

        return self.out_file

    @staticmethod
    def export_step(out_directory: Path) -> Path:
        """Export STEP from CadQuery model."""
        pathname = out_directory / "result.step"
        cq_object = FinalAssembly().cq_object.toCompound()

        export = ExportWrapper()

        export(
            cq_object,
            pathname,
            tolerance=0.01,
            angular_tolerance=0.1,
        )

        return pathname

    @staticmethod
    def create_mayo_config(
        height: int, width: int, mayo_config: dict[str, Any] | None = None
    ) -> ConfigParser:
        """Create mayo config.

        Mayo config file keys are case-sensitive. To prevent ``configparser`` from
        forcing keys to lower-case ``configparser.RawConfigParser.optionxform`` is
        monkey patched.
        """
        config = ConfigParser()

        # allow mixed case keys
        config.optionxform = lambda optionstr: optionstr  # type: ignore[assignment]

        config["application"] = {
            "language": "en",
        }

        config["export"] = {
            "Image\\backgroundColor": "#000000",
            "Image\\cameraOrientation": "1, -1, 1",
            "Image\\cameraProjection": "Orthographic",
            "Image\\height": str(height),
            "Image\\width": str(width),
        }

        if mayo_config is not None:
            config.read_dict(mayo_config)

        return config

    @staticmethod
    def export_png(mayo_config_pathname: Path, in_file: Path) -> Path:
        """Export PNG image from STEP file."""
        out_file = Path(in_file.parent / "exported-from-step.png")

        result = run(
            [
                "mayo",
                "--settings",
                mayo_config_pathname,
                in_file,
                "--export",
                out_file,
            ],
            capture_output=True,
            text=True,
        )
        result.check_returncode()

        return out_file

    @staticmethod
    def optimise_png(in_file: Path) -> None:
        """Optimise PNG with optipng."""
        result = run(
            [
                "optipng",
                in_file,
            ],
            capture_output=True,
            text=True,
        )
        result.check_returncode()

    def label_image(self, image: Image, text: str, font_size: int = 20) -> Image:
        """Label image."""
        font = ImageFont.truetype(str(self.font_path), font_size)

        label_bg_color = (255, 255, 255)
        label_fg_color = (0, 0, 0)

        left, top, right, bottom = font.getbbox(text)
        del left, right

        text_height = bottom - top
        label_height = ceil(text_height * 1.2)

        label = Image.new(image.mode, (image.width, label_height), label_bg_color)
        label_draw = ImageDraw.Draw(label)
        label_draw.text(
            (label.width / 2, label.height / 2),
            text,
            label_fg_color,
            font=font,
            anchor="mm",
        )

        result = Image.new(image.mode, (image.width, image.height + label.height))
        result.paste(image, (0, 0))
        result.paste(label, (0, image.height))

        return result

    def exif_tags(self) -> Exif:
        """Create EXIF tags."""
        # build reverse dict
        _TAGS_r = dict(((v, k) for k, v in TAGS.items()))
        tags = Exif()

        tags[_TAGS_r["Artist"]] = COPYRIGHT_OWNER
        tags[_TAGS_r["Copyright"]] = COPYRIGHT_NOTICE
        tags[_TAGS_r["DateTime"]] = self.now.strftime(self.EXIF_DATE_FORMAT)
        tags[_TAGS_r["DateTimeDigitized"]] = self.now.strftime(self.EXIF_DATE_FORMAT)
        tags[_TAGS_r["DateTimeOriginal"]] = self.now.strftime(self.EXIF_DATE_FORMAT)
        tags[_TAGS_r["ImageDescription"]] = LONG_DESCRIPTION
        tags[_TAGS_r["Software"]] = PROJECT_URL

        return tags
