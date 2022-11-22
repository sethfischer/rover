"""Rocker axle assembly."""

from __future__ import annotations

import cadquery as cq

from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import Commodity, PartIdentifier, PartTypes
from osr_mechanical.cq_containers import CqAssemblyContainer
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS
from osr_warehouse.generic.linear_motion.shf import SHF
from osr_warehouse.materials import COLORS


class RockerAxle(CqAssemblyContainer):
    """Rocker axle assembly."""

    AXLE_DIAMETER = 8
    AXLE_PROTRUSION = 40

    def __init__(self) -> None:
        """Initialise rocker axle assembly."""
        self.axle_length = FRAME_DIMENSIONS.WIDTH + (2 * self.AXLE_PROTRUSION)

        self.axle_support = SHF(self.AXLE_DIAMETER)

        self.chrome_plate = cq.Color(*COLORS["chrome_plate"])
        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])

        self._cq_object = self._make()

    def _make(self) -> cq.Assembly:
        """Make assembly."""
        axle = cq.Workplane("YZ").cylinder(self.axle_length, self.AXLE_DIAMETER / 2)
        axle_support = self.axle_support.cq_object

        flange_face_to_origin = FRAME_DIMENSIONS.WIDTH / 2 - 20

        result = (
            cq.Assembly(
                name="rocker_axle",
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
            )
            .add(
                axle_support,
                name="rocker_axle__support_port",
                loc=cq.Location(
                    cq.Vector(flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    -90,
                ),
            )
            .add(
                axle_support,
                name="rocker_axle__support_starboard",
                loc=cq.Location(
                    cq.Vector(-flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                axle,
                name="rocker_axle__axle",
                color=self.aluminium_cast,
            )
        )

        return result

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        support = PartIdentifier(
            PartTypes.linear_motion,
            "SHF8-SUPP",
            Commodity.PURCHASED,
            self.axle_support.description,
        )
        axle = PartIdentifier(
            PartTypes.linear_motion,
            "SHF-AXLE",
            Commodity.FABRICATED,
            (
                f"Chromed linear shaft: "
                f"⌀{self.AXLE_DIAMETER}mm, length={self.axle_length}mm."
            ),
        )

        return {
            "rocker_axle__support_port": support,
            "rocker_axle__support_starboard": support,
            "rocker_axle__axle": axle,
        }
