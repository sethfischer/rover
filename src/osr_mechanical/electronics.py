"""Electronics mounted on DIN rail."""

from __future__ import annotations

import cadquery as cq
from cq_electronics.mechanical.din_clip import DinClip
from cq_electronics.mechanical.din_rail import TopHat
from cq_electronics.rpi.rpi3b import RPi3b
from cq_electronics.sourcekit.pitray_clip import PiTrayClip

from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import PartIdentifier, PartTypes
from osr_mechanical.cq_containers import CqAssemblyContainer
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS
from osr_warehouse.materials import COLORS


class ControlElectronics(CqAssemblyContainer):
    """Control electronics mounted on DIN rail."""

    END_CLEARANCE = 2

    def __init__(self) -> None:
        """Initialise."""
        self._name = "electronics_control"

        self.din_rail_length = FRAME_DIMENSIONS.WIDTH - (2 * self.END_CLEARANCE)

        self.din_rail = TopHat(self.din_rail_length)
        self.raspberry_pi = RPi3b()
        self.pitray_clip = PiTrayClip()

        self._cq_object = self._make()

    def _make(self) -> cq.Assembly:
        """Make control electronics assembly."""
        rpi_x_offset = -50

        pitray_clip_z = (
            PiTrayClip.HEIGHT / 2
            + DinClip.HEIGHT
            - DinClip.RAIL_APERTURE_DEPTH
            + self.din_rail.depth / 2
        )

        rpi_x = -(
            abs(rpi_x_offset)
            - PiTrayClip.WIDTH / 2
            + self.pitray_clip.pcb_screw_cylinder_length
            + RPi3b.THICKNESS / 2
            + RPi3b.SOLDER_MASK_THICKNESS
        )
        rpi_z = (
            RPi3b.HEIGHT / 2
            - RPi3b.HOLE_OFFSET_FROM_EDGE
            + self.din_rail.depth / 2
            + DinClip.HEIGHT
            - DinClip.RAIL_APERTURE_DEPTH
            + PiTrayClip.HEIGHT
            - self.pitray_clip.pcb_screw_cylinder_from_edge
        )

        result = (
            cq.Assembly(
                name=self.name,
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
            )
            .add(
                self.din_rail.cq_object,
                name=self.sub_assembly_name("din_rail"),
                color=cq.Color(*COLORS["aluminium_anodised_natural"]),
            )
            .add(
                self.pitray_clip.cq_object,
                name=self.sub_assembly_name("pitray_clip"),
                loc=cq.Location(
                    cq.Vector(rpi_x_offset, -8, pitray_clip_z),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                self.raspberry_pi.cq_object,
                name=self.sub_assembly_name("rpi"),
                loc=cq.Location(
                    cq.Vector(rpi_x, 2, rpi_z),
                    cq.Vector(0, 1, 0),
                    -90,
                ),
            )
        )

        return result

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        din_rail = PartIdentifier(
            PartTypes.din,
            "RAIL-75",
            f"DIN rail: 35×7.5mm, length={self.din_rail.length}mm.",
        )
        pitray_clip = PartIdentifier(
            PartTypes.din,
            "CLIP-RPI",
            "DIN rail clip: to suit Raspberry Pi 3B.",
        )
        rpi = PartIdentifier(
            PartTypes.electronic,
            "RPI3B",
            "Raspberry Pi 3B single board computer.",
        )

        return {
            self.sub_assembly_name("din_rail"): din_rail,
            self.sub_assembly_name("pitray_clip"): pitray_clip,
            self.sub_assembly_name("rpi"): rpi,
        }
