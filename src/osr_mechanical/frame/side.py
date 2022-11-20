"""Frame side assembly."""

from __future__ import annotations

import cadquery as cq

from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import Commodity, NauticalSide, PartIdentifier, PartTypes
from osr_mechanical.cqobject import CqAssemblyContainer
from osr_mechanical.frame.dimensions import FRAME_DIMENSIONS as DIM
from osr_warehouse.alexco import Vslot2020, Vslot2040
from osr_warehouse.fasteners import M5_CLEARANCE_CLOSE_DIAMETER, M5_COUNTERBORE_DIAMETER
from osr_warehouse.generic.linear_motion.shf import SHFSeriesDimensions
from osr_warehouse.materials import COLORS


class FrameSide(CqAssemblyContainer):
    """Frame side assembly."""

    def __init__(
        self, nautical_side: NauticalSide, simple: bool = False, fasteners: bool = True
    ) -> None:
        """Initialise."""
        self.simple = simple
        self.nautical_side = nautical_side
        self.fasteners = fasteners

        self.between_shf_mounting_holes = (
            SHFSeriesDimensions.shf8.between_mounting_holes
        )

        self.pillar_transom_height = DIM.HEIGHT + DIM.TRANSOM_HEIGHT

        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])
        self.aluminium_anodised_natural = cq.Color(
            *COLORS["aluminium_anodised_natural"]
        )

        self._cq_object = self._make()

    @property
    def cq_object(self) -> cq.Assembly:
        """Get CadQuery object."""
        return self._cq_object

    def cq_part(self, name: str) -> cq.Shape | cq.Workplane:
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception("Part is not a valid Shape or Workplane.")

        return result

    @staticmethod
    def _make_beam_side(
        length: float,
        deck: bool = True,
        differential_pivot_beam_offset: float | None = None,
    ):
        """Create side beam."""
        beam_fore_y = (-(DIM.TRANSOM_LENGTH - Vslot2020.WIDTH) - DIM.LENGTH) / 2
        hole_fore_y = beam_fore_y + (Vslot2020.WIDTH / 2)
        hole_fore_rocker_pillar_y = (
            beam_fore_y + DIM.ROCKER_AXLE_DISTANCE_FROM_FORE - Vslot2040.WIDTH / 2
        )

        result = Vslot2020().make(length)

        result = (
            result.faces(">X")
            .workplane(centerOption="CenterOfMass")
            .tag("workplane_lateral_holes")
            .center(0, hole_fore_y)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_fore")
            .center(0, DIM.LENGTH - Vslot2020.WIDTH)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_aft")
        )

        if deck:
            rocker_pillar_hole_face_selector = ">Y"
        else:
            rocker_pillar_hole_face_selector = "<Y"

        result = (
            result.faces(rocker_pillar_hole_face_selector)
            .workplane(centerOption="CenterOfMass")
            .tag("workplane_rocker_pillar_holes")
            .center(0, hole_fore_rocker_pillar_y)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_fore_rocker_pillar")
            .center(0, Vslot2040.DISTANCE_BETWEEN_CENTERS)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_aft_rocker_pillar")
        )

        if differential_pivot_beam_offset is not None:
            hole_beam_differential_pivot_y = (
                beam_fore_y
                + DIM.DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE
                + differential_pivot_beam_offset
            )

            result = (
                result.workplaneFromTagged("workplane_lateral_holes")
                .center(0, hole_beam_differential_pivot_y)
                .cboreHole(
                    M5_CLEARANCE_CLOSE_DIAMETER,
                    M5_COUNTERBORE_DIAMETER,
                    Vslot2020.COUNTERBORE_DEPTH,
                    depth=None,
                )
                .tag("hole_beam_differential_pivot")
            )

        return result

    def _make_pillar_rocker(self, height: float):
        """Create rocker axle pillar."""
        half_between_shf_mounting_holes = self.between_shf_mounting_holes / 2
        shf_mounting_hole_points = [
            (0, half_between_shf_mounting_holes),
            (0, -half_between_shf_mounting_holes),
        ]
        return (
            Vslot2040()
            .make(height)
            .faces("<Y")
            .workplane(centerOption="CenterOfMass")
            .center(0, 0)
            .circle((DIM.ROCKER_AXLE_DIAMETER / 2) + DIM.ROCKER_AXLE_CLEARANCE)
            .tag("rocker_axle_clearance_hole")
            .extrude(-Vslot2040.WIDTH, combine="s")
            .pushPoints(shf_mounting_hole_points)
            .hole(M5_CLEARANCE_CLOSE_DIAMETER)
        )

    @staticmethod
    def _make_pillar_transom(height: float):
        """Create transom pillar."""
        return (
            Vslot2020()
            .make(height)
            .faces(">X")
            .workplane(centerOption="ProjectedOrigin")
            .center(0, Vslot2020.WIDTH / 2)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_belly")
            .center(0, DIM.HEIGHT - Vslot2020.WIDTH)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_deck")
        )

    def _make(self) -> cq.Assembly:
        """Create assembly."""
        pillar_rocker = self._make_pillar_rocker(DIM.PILLAR_HEIGHT)
        pillar_transom = self._make_pillar_transom(self.pillar_transom_height)

        beam_deck = self._make_beam_side(
            DIM.BEAM_SIDE_LENGTH,
            deck=True,
            differential_pivot_beam_offset=DIM.DIFFERENTIAL_PIVOT_BEAM_OFFSET,
        )
        beam_belly = self._make_beam_side(DIM.BEAM_SIDE_LENGTH, deck=False)

        beam_deck = beam_deck.rotateAboutCenter((0, 0, 1), 180)
        beam_belly = beam_belly.rotateAboutCenter((0, 0, 1), 180)

        if self.nautical_side.name == "port":
            beam_deck = beam_deck.mirror("ZY")
            beam_belly = beam_belly.mirror("ZY")

        assembly = (
            cq.Assembly(
                name=f"frame_side_{self.nautical_side.name}",
                metadata={Bom.PARTS_KEY: self.part_identifiers()},
                color=self.aluminium_anodised_natural,
            )
            .add(
                pillar_transom,
                name=f"frame_side_{self.nautical_side.name}__pillar_transom",
                loc=cq.Location(
                    cq.Vector(
                        0,
                        DIM.LENGTH + DIM.TRANSOM_LENGTH - Vslot2020.WIDTH / 2,
                        0,
                    ),
                    cq.Vector(0, 0, 1),
                    90,
                ),
            )
            .add(
                pillar_rocker,
                name=f"frame_side_{self.nautical_side.name}__pillar_rocker",
                loc=cq.Location(
                    cq.Vector(
                        0,
                        DIM.ROCKER_AXLE_DISTANCE_FROM_FORE,
                        Vslot2020.WIDTH,
                    ),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                beam_belly,
                name=f"frame_side_{self.nautical_side.name}__beam_belly",
                loc=cq.Location(
                    cq.Vector(
                        0,
                        0,
                        Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(1, 0, 0),
                    -90,
                ),
            )
            .add(
                beam_deck,
                name=f"frame_side_{self.nautical_side.name}__beam_deck",
                loc=cq.Location(
                    cq.Vector(
                        0,
                        0,
                        DIM.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(1, 0, 0),
                    -90,
                ),
            )
        )

        return assembly

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        pillar_transom = PartIdentifier(
            PartTypes.tslot,
            "PILLAR-TRANS",
            Commodity.FABRICATED,
            (
                f"Frame transom pillar: "
                f"T-slot {Vslot2020.WIDTH}×{Vslot2020.HEIGHT}mm, "
                f"length={self.pillar_transom_height}mm."
            ),
        )
        pillar_rocker = PartIdentifier(
            PartTypes.tslot,
            "PILLAR-ROCK",
            Commodity.FABRICATED,
            (
                f"Frame rocker axle pillar: "
                f"T-slot {Vslot2040.WIDTH}×{Vslot2040.HEIGHT}mm, "
                f"length={DIM.PILLAR_HEIGHT}mm."
            ),
        )
        beam_belly = PartIdentifier(
            PartTypes.tslot,
            "BEAM-BELLY",
            Commodity.FABRICATED,
            (
                f"Frame belly beam {self.nautical_side.name}: "
                f"T-slot {Vslot2020.WIDTH}×{Vslot2020.HEIGHT}mm, "
                f"length={DIM.BEAM_SIDE_LENGTH}mm."
            ),
            self.nautical_side.identifier,
        )
        beam_deck = PartIdentifier(
            PartTypes.tslot,
            "BEAM-DECK",
            Commodity.FABRICATED,
            (
                f"Frame deck beam {self.nautical_side.name}: "
                f"T-slot {Vslot2020.WIDTH}×{Vslot2020.HEIGHT}mm, "
                f"length={DIM.BEAM_SIDE_LENGTH}mm."
            ),
            self.nautical_side.identifier,
        )

        return {
            f"frame_side_{self.nautical_side.name}__pillar_transom": pillar_transom,
            f"frame_side_{self.nautical_side.name}__pillar_rocker": pillar_rocker,
            f"frame_side_{self.nautical_side.name}__beam_belly": beam_belly,
            f"frame_side_{self.nautical_side.name}__beam_deck": beam_deck,
        }
