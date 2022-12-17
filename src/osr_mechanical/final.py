"""Final assembly."""

from __future__ import annotations

import cadquery as cq

from osr_common.cq_containers import CqAssemblyContainer
from osr_mechanical.bom.parts import PartIdentifier
from osr_mechanical.electronics import ControlElectronics
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS
from osr_mechanical.frame.final import Frame
from osr_mechanical.rocker_axle import RockerAxle
from osr_warehouse.alexco.vslot import Vslot2020


class FinalAssembly(CqAssemblyContainer):
    """Final assembly."""

    def __init__(self, *, simple: bool = False):
        """Initialise FinalAssembly."""
        self.simple = simple

        self._name = "final"

        self.frame = Frame(simple=self.simple)
        self.rocker_axle = RockerAxle()
        self.control_electronics = ControlElectronics()

        self._cq_object = self._make()

    def _make(self) -> cq.Assembly:
        """Make assembly."""
        control_electronics_loc = cq.Location(
            cq.Vector(
                self.control_electronics.din_rail.length / 2,
                80,
                Vslot2020.WIDTH + self.control_electronics.din_rail.depth / 2,
            ),
        )

        result = (
            cq.Assembly(name=self.name)
            .add(
                self.frame.cq_object,
                name=self.sub_assembly_name("frame"),
            )
            .add(
                self.rocker_axle.cq_object,
                name=self.sub_assembly_name("rocker_axle"),
                loc=cq.Location(
                    cq.Vector(
                        0,
                        FRAME_DIMENSIONS.ROCKER_AXLE_DISTANCE_FROM_FORE,
                        FRAME_DIMENSIONS.HEIGHT / 2,
                    ),
                ),
            )
            .add(
                self.control_electronics.cq_object,
                name=self.sub_assembly_name("control_electronics"),
                loc=control_electronics_loc,
            )
        )

        return result

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        return {}
