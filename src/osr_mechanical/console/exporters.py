"""Custom exporters."""

import configparser
import tempfile
from datetime import datetime
from math import ceil
from pathlib import Path
from typing import Any, Dict, Union

from cadquery import exporters
from invoke import Context
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS
from PIL.Image import Exif

from osr_mechanical.config import COPYRIGHT_OWNER, PROJECT_HOST, PROJECT_URL
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
        mayo_config: Union[Dict[str, Any], None] = None,
        label: bool = True,
    ) -> None:
        """Initialise exporter."""
        self.out_file = out_file
        self.width = width
        self.height = height
        self.mayo_config = mayo_config
        self.label = label

        self.font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

    def export(self) -> Path:
        """Export PNG image."""
        context = Context()

        with tempfile.TemporaryDirectory() as tmp_directory_name:
            tmp_directory = Path(tmp_directory_name)
            with context.cd(str(tmp_directory)):
                step_pathname = self.export_step(tmp_directory)

                mayo_config = self.create_mayo_config(
                    self.height, self.width, self.mayo_config
                )
                mayo_config_pathname = Path(tmp_directory / "mayo.ini")
                with open(str(mayo_config_pathname), "w") as file:
                    mayo_config.write(file)

                exported_png = self.export_png(
                    context, mayo_config_pathname, step_pathname
                )

                result_path = Path(tmp_directory / "result.png")
                image = Image.open(exported_png)

                if self.label:
                    label = f"{PROJECT_HOST}    {datetime.today().strftime('%Y-%m-%d')}"
                    image = self.label_image(image, label)

                exif = self.exif_tags()
                image.save(result_path, exif=exif)

                result_path.rename(self.out_file)

        return self.out_file

    @staticmethod
    def export_step(out_directory: Path) -> Path:
        """Export STEP from CadQuery model."""
        pathname = out_directory / "result.step"

        exporters.export(
            FinalAssembly().cq_object.toCompound(),
            str(pathname),
            tolerance=0.01,
            angularTolerance=0.1,
        )

        return pathname

    @staticmethod
    def create_mayo_config(
        height: int, width: int, mayo_config: Union[Dict[str, Any], None] = None
    ) -> configparser.ConfigParser:
        """Create mayo config.

        Mayo config file keys are case-sensitive. To prevent ``configparser`` from
        forcing keys to lower-case ``configparser.RawConfigParser.optionxform`` is
        monkey patched.
        """
        config = configparser.ConfigParser()

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
    def export_png(context: Context, mayo_config_pathname: Path, in_file: Path) -> Path:
        """Export PNG image from STEP file."""
        out_file = Path(in_file.parent / "exported-from-step.png")

        command = (
            f"mayo --settings {mayo_config_pathname} {in_file} --export {out_file}"
        )
        context.run(command, hide=True, warn=True)

        return out_file

    def label_image(self, image: Image, text: str, font_size: int = 20) -> Image:
        """Label image."""
        font = ImageFont.truetype(str(self.font_path), font_size)

        label_bg_color = (255, 255, 255)
        label_fg_color = (0, 0, 0)
        text_width, text_height = font.getsize(text)
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
        now = datetime.today()
        tags = Exif()

        copyright_notice = (
            f"(c) {now.strftime('%Y')} {COPYRIGHT_OWNER}; Licence: MIT License"
        )
        description = (
            "Final assembly of sethfischer-osr, a quarter-scale Mars rover. "
            f"See <{PROJECT_URL}>. "
            "Based on NASA-JPL's Perseverance Mars Rover."
        )

        tags[_TAGS_r["Artist"]] = COPYRIGHT_OWNER
        tags[_TAGS_r["Copyright"]] = copyright_notice
        tags[_TAGS_r["DateTime"]] = now.strftime(self.EXIF_DATE_FORMAT)
        tags[_TAGS_r["DateTimeDigitized"]] = now.strftime(self.EXIF_DATE_FORMAT)
        tags[_TAGS_r["DateTimeOriginal"]] = now.strftime(self.EXIF_DATE_FORMAT)
        tags[_TAGS_r["ImageDescription"]] = description
        tags[_TAGS_r["Software"]] = PROJECT_URL

        return tags