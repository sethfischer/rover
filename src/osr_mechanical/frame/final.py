"""Frame assembly."""

from typing import Union

import cadquery as cq

from osr_mechanical.bom.parts import PartIdentifier, port, starboard
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS as DIM
from osr_mechanical.frame.fore import FrameFore
from osr_mechanical.frame.pivot_beam import FramePivotBeam
from osr_mechanical.frame.side import FrameSide
from osr_warehouse.alexco.vslot import Vslot2020
from osr_warehouse.cqobject import CqAssemblyContainer


class Frame(CqAssemblyContainer):
    """Frame assembly."""

    def __init__(self, simple: bool = False):
        """Initialise."""
        self.simple = simple

        self.beam_lateral = Vslot2020().make(DIM.LATERAL_BEAM_LENGTH)
        self.beam_pivot = FramePivotBeam()
        self.fore = FrameFore()
        self.side_port = FrameSide(port)
        self.side_starboard = FrameSide(starboard)

        self._cq_object = self._make()

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    def cq_part(self, name: str) -> Union[cq.Shape, cq.Workplane]:
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception("Part is not a valid Shape or Workplane.")

        return result

    def _make(self) -> cq.Assembly:
        """Make assembly."""
        side_x_offset = (DIM.WIDTH - Vslot2020.WIDTH) / 2

        result = (
            cq.Assembly(name="frame")
            .add(
                self.side_starboard.cq_object,
                name="frame__side_starboard",
                loc=cq.Location(cq.Vector(-side_x_offset, 0, 0)),
            )
            .add(
                self.side_port.cq_object,
                name="frame__side_port",
                loc=cq.Location(cq.Vector(side_x_offset, 0, 0)),
            )
            .add(
                self.fore.cq_object,
                name="frame__fore",
            )
            .add(
                self.beam_pivot.cq_object,
                name="frame__beam_pivot",
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        DIM.DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE,
                        DIM.HEIGHT,
                    )
                ),
            )
            .add(
                self.beam_lateral,
                name="frame__beam_lateral_deck",
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        DIM.LENGTH - Vslot2020.WIDTH / 2,
                        DIM.HEIGHT - Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                self.beam_lateral,
                name="frame__beam_lateral_belly",
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        DIM.LENGTH - Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
        )

        return result

    def bom_parts(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        return {}
