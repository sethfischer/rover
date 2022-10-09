"""Final assembly."""
from typing import Any

import cadquery as cq

from osr_mechanical.electronics import ControlElectronics
from osr_mechanical.frame import Frame
from osr_mechanical.rocker_axle import RockerAxle
from osr_warehouse.alexco.vslot import Vslot2020
from osr_warehouse.cqobject import CqAssemblyContainer


class FinalAssembly(CqAssemblyContainer):
    """Final assembly."""

    def __init__(self, simple: bool = False):
        """Initialise final assembly."""
        self.simple = simple

        self.frame = Frame(simple=self.simple)
        self.rocker_axle = RockerAxle()
        self.control_electronics = ControlElectronics()

        self._cq_object = self.make()

    def cq_part(self, name: str) -> Any:
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception("Part is not a valid Shape or Workplane.")

        return result

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    def make(self) -> cq.Assembly:
        """Make assembly."""
        control_electronics_loc = cq.Location(
            cq.Vector(
                self.control_electronics.din_rail.length / 2,
                70,
                Vslot2020.WIDTH + self.control_electronics.din_rail.depth / 2,
            ),
        )

        result = (
            cq.Assembly()
            .add(
                self.frame.cq_object,
                name="frame_assembly",
            )
            .add(
                self.rocker_axle.cq_object,
                name="rocker_axle_assembly",
                loc=cq.Location(
                    cq.Vector(
                        0, Frame.ROCKER_AXLE_DISTANCE_FROM_FORE - 10, Frame.HEIGHT / 2
                    ),
                ),
            )
            .add(
                self.control_electronics.cq_object,
                name="control_electronics",
                loc=control_electronics_loc,
            )
        )

        return result
