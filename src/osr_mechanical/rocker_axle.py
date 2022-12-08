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
        """Initialise RockerAxle."""
        self._name = "rocker_axle"

        self.axle_length = FRAME_DIMENSIONS.WIDTH + (2 * self.AXLE_PROTRUSION)

        self.axle_pillar = SHF(self.AXLE_DIAMETER)

        self.chrome_plate = cq.Color(*COLORS["chrome_plate"])
        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])

        self._cq_object = self._make()

    def _make(self) -> cq.Assembly:
        """Make assembly."""
        axle = cq.Workplane("YZ").cylinder(self.axle_length, self.AXLE_DIAMETER / 2)
        axle_pillar = self.axle_pillar.cq_object

        flange_face_to_origin = FRAME_DIMENSIONS.WIDTH / 2 - 20

        result = (
            cq.Assembly(
                name=self.name,
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
            )
            .add(
                axle_pillar,
                name=self.sub_assembly_name("pillar_port"),
                loc=cq.Location(
                    cq.Vector(flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    -90,
                ),
            )
            .add(
                axle_pillar,
                name=self.sub_assembly_name("pillar_starboard"),
                loc=cq.Location(
                    cq.Vector(-flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                axle,
                name=self.sub_assembly_name("axle"),
                color=self.aluminium_cast,
            )
        )

        return result

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        pillar = PartIdentifier(
            PartTypes.linear_motion,
            "SHF8-PILLAR",
            self.axle_pillar.description,
        )
        axle = PartIdentifier(
            PartTypes.linear_motion,
            "SHF-AXLE",
            (
                f"Chromed linear shaft: "
                f"⌀{self.AXLE_DIAMETER}mm, length={self.axle_length}mm."
            ),
            Commodity.FABRICATED,
        )

        return {
            self.sub_assembly_name("pillar_port"): pillar,
            self.sub_assembly_name("pillar_starboard"): pillar,
            self.sub_assembly_name("axle"): axle,
        }
