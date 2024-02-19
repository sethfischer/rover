"""Rocker axle assembly."""

import cadquery as cq

from osr_common.cq_containers import CqAssemblyContainer
from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import Commodity, PartIdentifier, PartTypes
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

        self.shaft_support = SHF(self.AXLE_DIAMETER)

        self.chrome_plate = cq.Color(*COLORS["chrome_plate"])
        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])

        self._cq_object = self._make()

    def _make(self) -> cq.Assembly:
        """Make assembly."""
        axle = cq.Workplane("YZ").cylinder(self.axle_length, self.AXLE_DIAMETER / 2)
        shaft_support = self.shaft_support.cq_object

        flange_face_to_origin = FRAME_DIMENSIONS.WIDTH / 2 - 20

        result = (
            cq.Assembly(
                name=self.name,
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
            )
            .add(
                shaft_support,
                name=self.sub_assembly_name("shf_port"),
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    -90,
                ),
            )
            .add(
                shaft_support,
                name=self.sub_assembly_name("shf_starboard"),
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(-flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                axle,
                name=self.sub_assembly_name("axle"),
                color=self.chrome_plate,
            )
        )

        return result

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        shaft_support = PartIdentifier(
            PartTypes.linear_motion,
            "SHF8FLANGE",
            self.shaft_support.description,
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
            self.sub_assembly_name("shf_port"): shaft_support,
            self.sub_assembly_name("shf_starboard"): shaft_support,
            self.sub_assembly_name("axle"): axle,
        }
