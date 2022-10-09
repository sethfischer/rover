"""Rocker axle assembly."""
from typing import Any

import cadquery as cq

from osr_mechanical.frame import Frame
from osr_warehouse.cqobject import CqAssemblyContainer
from osr_warehouse.generic.linear_motion.shf import SHF
from osr_warehouse.materials import COLORS


class RockerAxle(CqAssemblyContainer):
    """Rocker axle assembly."""

    AXLE_DIAMETER = 8
    AXLE_PROTRUSION = 40

    def __init__(self) -> None:
        """Initialise rocker axle assembly."""
        self.axle_length = Frame.WIDTH + (2 * self.AXLE_PROTRUSION)

        self.chrome_plate = cq.Color(*COLORS["chrome_plate"])
        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])

        self._cq_object = self._make()

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

    def _make(self) -> cq.Assembly:
        """Make assembly."""
        axle = cq.Workplane("YZ").cylinder(self.axle_length, self.AXLE_DIAMETER / 2)
        axle_support = SHF(self.AXLE_DIAMETER).cq_object

        flange_face_to_origin = Frame.WIDTH / 2 - 20

        result = (
            cq.Assembly()
            .add(
                axle_support,
                name="rocker_axle_support_port",
                loc=cq.Location(
                    cq.Vector(flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    -90,
                ),
            )
            .add(
                axle_support,
                name="rocker_axle_support_starboard",
                loc=cq.Location(
                    cq.Vector(-flange_face_to_origin, 0, 0),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                axle,
                name="rocker_axle",
                color=self.aluminium_cast,
            )
        )

        return result
