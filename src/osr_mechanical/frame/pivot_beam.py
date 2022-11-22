"""Differential pivot beam assembly."""

from __future__ import annotations

import cadquery as cq

from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import Commodity, PartIdentifier, PartTypes
from osr_mechanical.cq_containers import CqAssemblyContainer
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS as DIM
from osr_warehouse.alexco import Vslot2020
from osr_warehouse.generic.vslot.brackets2020 import (
    StandardStandardDuty90 as BracketStandardStandardDuty90,
)
from osr_warehouse.materials import COLORS


class FramePivotBeam(CqAssemblyContainer):
    """Differential pivot beam assembly."""

    def __init__(self, simple: bool = False) -> None:
        """Initialise."""
        self.simple = simple

        self.bracket_standard_duty = BracketStandardStandardDuty90()

        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])
        self.aluminium_anodised_natural = cq.Color(
            *COLORS["aluminium_anodised_natural"]
        )

        self._cq_object = self._make()

    def _make(self) -> cq.Assembly:
        """Create assembly."""
        beam_differential_pivot = Vslot2020().make(DIM.LATERAL_BEAM_LENGTH)

        bracket_y_offset = Vslot2020.WIDTH / 2
        z_offset = Vslot2020.WIDTH / 2

        assembly = (
            cq.Assembly(
                name="frame_beam_pivot",
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
                color=self.aluminium_anodised_natural,
            )
            .add(
                beam_differential_pivot,
                name="frame_beam_pivot__beam",
                loc=cq.Location(
                    cq.Vector(0, 0, -z_offset),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                self.bracket_standard_duty.cq_object,
                name="frame_beam_pivot__bracket_starboard",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(0, bracket_y_offset, -z_offset),
                    cq.Vector(-1, 0, 0),
                    90,
                ),
            )
            .add(
                self.bracket_standard_duty.cq_object.mirror("YZ"),
                name="frame_beam_pivot__bracket_port",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        DIM.LATERAL_BEAM_LENGTH,
                        bracket_y_offset,
                        -z_offset,
                    ),
                    cq.Vector(-1, 0, 0),
                    90,
                ),
            )
        )

        return assembly

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        beam_differential_pivot = PartIdentifier(
            PartTypes.tslot,
            "BEAM-DIFF",
            Commodity.FABRICATED,
            (
                f"Frame beam differential pivot: "
                f"T-slot {Vslot2020.WIDTH}×{Vslot2020.HEIGHT}mm, "
                f"length={DIM.LATERAL_BEAM_LENGTH}mm."
            ),
        )
        bracket_standard_duty = PartIdentifier(
            PartTypes.tslot,
            "BRACKET-SD",
            Commodity.PURCHASED,
            self.bracket_standard_duty.description,
        )

        return {
            "frame_beam_pivot__beam": beam_differential_pivot,
            "frame_beam_pivot__bracket_starboard": bracket_standard_duty,
            "frame_beam_pivot__bracket_port": bracket_standard_duty,
        }
