"""Frame fore assembly."""

from __future__ import annotations

import cadquery as cq

from osr_common.cq_containers import CqAssemblyContainer
from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import Commodity, PartIdentifier, PartTypes
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS as DIM
from osr_warehouse.alexco import Vslot2020
from osr_warehouse.generic.vslot.brackets2020 import (
    StandardLightDuty90 as BracketStandardLightDuty90,
)
from osr_warehouse.materials import COLORS


class FrameFore(CqAssemblyContainer):
    """Frame fore assembly."""

    def __init__(self, simple: bool = False) -> None:
        """Initialise FrameFore."""
        self.simple = simple

        self._name = "frame_fore"

        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])
        self.aluminium_anodised_natural = cq.Color(
            *COLORS["aluminium_anodised_natural"]
        )

        self.bracket_light_duty = BracketStandardLightDuty90()

        self._cq_object = self._make()

    @staticmethod
    def _make_beam_lateral(length: float) -> cq.Workplane:
        """Create lateral beam."""
        return Vslot2020().make(length)

    @staticmethod
    def _make_pillar(height: float) -> cq.Workplane:
        """Create pillar."""
        return Vslot2020().make(height)

    def _make(self) -> cq.Assembly:
        """Create assembly."""
        pillar_fore = self._make_pillar(DIM.PILLAR_HEIGHT)
        beam_lateral = self._make_beam_lateral(DIM.LATERAL_BEAM_LENGTH)

        # position starboard pillar
        # rotate to place center bore slot on inside of frame
        # translate in X direction so base is on the XY plane
        pillar_starboard = pillar_fore.rotateAboutCenter((0, 0, 1), 180).translate(
            (
                -DIM.LATERAL_BEAM_LENGTH / 2 - Vslot2020.WIDTH / 2,
                Vslot2020.WIDTH / 2,
                Vslot2020.WIDTH,
            )
        )

        assembly = (
            cq.Assembly(
                name=self.name,
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
                color=self.aluminium_anodised_natural,
            )
            .add(
                pillar_starboard,
                name=self.sub_assembly_name("pillar_starboard"),
            )
            .add(
                pillar_fore,
                name=self.sub_assembly_name("pillar_port"),
                loc=cq.Location(
                    cq.Vector(
                        DIM.LATERAL_BEAM_LENGTH / 2 + Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH,
                    ),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                beam_lateral,
                name=self.sub_assembly_name("beam_belly"),
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                beam_lateral,
                name=self.sub_assembly_name("beam_deck"),
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        Vslot2020.WIDTH / 2,
                        DIM.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                self.bracket_light_duty.cq_object,
                name=self.sub_assembly_name("bracket_starboard_belly"),
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH,
                    )
                ),
            )
            .add(
                self.bracket_light_duty.cq_object.mirror("XY"),
                name=self.sub_assembly_name("bracket_starboard_deck"),
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        -DIM.LATERAL_BEAM_LENGTH / 2,
                        Vslot2020.WIDTH / 2,
                        DIM.HEIGHT - Vslot2020.WIDTH,
                    )
                ),
            )
            .add(
                self.bracket_light_duty.cq_object.mirror("ZY"),
                name=self.sub_assembly_name("bracket_port_belly"),
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        DIM.LATERAL_BEAM_LENGTH / 2,
                        Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH,
                    )
                ),
            )
            .add(
                self.bracket_light_duty.cq_object,
                name=self.sub_assembly_name("bracket_port_deck"),
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        DIM.LATERAL_BEAM_LENGTH / 2,
                        Vslot2020.WIDTH / 2,
                        DIM.HEIGHT - Vslot2020.WIDTH,
                    ),
                    cq.Vector(0, 1, 0),
                    180,
                ),
            )
        )

        return assembly

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        pillar_fore = PartIdentifier(
            PartTypes.tslot,
            "PILLAR-FORE",
            (
                f"Frame fore pillar: "
                f"T-slot "
                f"{Vslot2020.WIDTH}×{Vslot2020.HEIGHT}mm, length={DIM.PILLAR_HEIGHT}mm."
            ),
            Commodity.FABRICATED,
        )
        beam_lateral = PartIdentifier(
            PartTypes.tslot,
            "BEAM-LAT",
            (
                f"Frame deck beam lateral: "
                f"T-slot {Vslot2020.WIDTH}×{Vslot2020.HEIGHT}mm, "
                f"length={DIM.LATERAL_BEAM_LENGTH}mm."
            ),
            Commodity.FABRICATED,
        )
        bracket_light_duty = PartIdentifier(
            PartTypes.tslot,
            "BRACKET-LD",
            self.bracket_light_duty.description,
        )

        return {
            self.sub_assembly_name("pillar_starboard"): pillar_fore,
            self.sub_assembly_name("pillar_port"): pillar_fore,
            self.sub_assembly_name("beam_belly"): beam_lateral,
            self.sub_assembly_name("beam_deck"): beam_lateral,
            self.sub_assembly_name("bracket_starboard_belly"): bracket_light_duty,
            self.sub_assembly_name("bracket_starboard_deck"): bracket_light_duty,
            self.sub_assembly_name("bracket_port_belly"): bracket_light_duty,
            self.sub_assembly_name("bracket_port_deck"): bracket_light_duty,
        }
