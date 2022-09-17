"""Frame assembly.

Frame is constructed primarily from lengths of 2020 V-slot aluminum extrusion.
"""
from typing import Union

import cadquery as cq

from osr_warehouse.alexco import Vslot2020, Vslot2040
from osr_warehouse.cqobject import CqAssemblyContainer
from osr_warehouse.fasteners import M5_CLEARANCE_CLOSE_DIAMETER, M5_COUNTERBORE_DIAMETER
from osr_warehouse.generic.linear_motion.shf import SHFSeriesDimensions
from osr_warehouse.generic.vslot.brackets2020 import (
    StandardLightDuty90 as BracketStandardLightDuty90,
)
from osr_warehouse.generic.vslot.brackets2020 import (
    StandardStandardDuty90 as BracketStandardStandardDuty90,
)
from osr_warehouse.materials import COLORS


class Frame(CqAssemblyContainer):
    """Frame assembly."""

    LENGTH = 439
    WIDTH = 285
    HEIGHT = 115
    TRANSOM_LENGTH = 48
    TRANSOM_HEIGHT = 75

    ROCKER_AXLE_DISTANCE_FROM_FORE = 165
    ROCKER_AXLE_DIAMETER = 8
    ROCKER_AXLE_CLEARANCE = 3

    DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE = 250
    DIFFERENTIAL_PIVOT_BEAM_OFFSET = 0

    POST_HEIGHT = HEIGHT - (2 * Vslot2020.WIDTH)
    BEAM_SIDE_LENGTH = LENGTH + TRANSOM_LENGTH - Vslot2020.WIDTH

    BEAM_END_LENGTH = WIDTH - (2 * Vslot2020.WIDTH)

    def __init__(self, simple: bool = False, color: bool = False) -> None:
        """Initialise frame assembly."""
        self.simple = simple
        self.color = color

        self.aluminium_cast = cq.Color(*COLORS["aluminium_cast"])
        self.aluminium_anodised_natural = cq.Color(
            *COLORS["aluminium_anodised_natural"]
        )

        self.between_shf_mounting_holes = (
            SHFSeriesDimensions.shf8.between_mounting_holes
        )

        self._cq_object = self.make()

        if color:
            self._cq_object = self.color_assembly(self._cq_object)

    @property
    def cq_object(self):
        """Frame CadQuery assembly."""
        return self._cq_object

    def cq_part(self, name: str):
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception("Part is not a valid Shape or Workplane.")

        return result

    @staticmethod
    def _make_beam_differential_pivot(length: float):
        """Create differential pivot beam."""
        return Vslot2020().make(length)

    @staticmethod
    def _make_beam_end(length: float):
        """Create end beam."""
        return Vslot2020().make(length)

    def _make_beam_side(
        self, length: float, differential_pivot_beam_offset: Union[float, None] = None
    ):
        """Create side beam."""
        beam_fore_y = (-(self.TRANSOM_LENGTH - Vslot2020.WIDTH) - self.LENGTH) / 2
        hole_fore_y = beam_fore_y + (Vslot2020.WIDTH / 2)
        hole_fore_rocker_axle_post_y = (
            beam_fore_y + self.ROCKER_AXLE_DISTANCE_FROM_FORE - Vslot2040.WIDTH / 2
        )

        beam = Vslot2020().make(length)

        beam = (
            beam.faces(">X")
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
            .center(0, self.LENGTH - Vslot2020.WIDTH)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_aft")
        )

        beam = (
            beam.faces(">Y")
            .workplane(centerOption="CenterOfMass")
            .tag("workplane_rocker_axle_post_holes")
            .center(0, hole_fore_rocker_axle_post_y)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_fore_rocker_axle_post")
            .center(0, Vslot2040.DISTANCE_BETWEEN_CENTERS)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_aft_rocker_axle_post")
        )

        if differential_pivot_beam_offset is not None:
            hole_beam_differential_pivot_y = (
                beam_fore_y
                + self.DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE
                + differential_pivot_beam_offset
            )

            beam = (
                beam.workplaneFromTagged("workplane_lateral_holes")
                .center(0, hole_beam_differential_pivot_y)
                .cboreHole(
                    M5_CLEARANCE_CLOSE_DIAMETER,
                    M5_COUNTERBORE_DIAMETER,
                    Vslot2020.COUNTERBORE_DEPTH,
                    depth=None,
                )
                .tag("hole_beam_differential_pivot")
            )

        return beam

    @staticmethod
    def _make_post(height: float):
        """Create post."""
        return Vslot2020().make(height)

    def _make_post_rocker_axle(self, height: float):
        """Create rocker axle post."""
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
            .circle((self.ROCKER_AXLE_DIAMETER / 2) + self.ROCKER_AXLE_CLEARANCE)
            .tag("rocker_axle_clearance_hole")
            .extrude(-Vslot2040.WIDTH, combine="s")
            .pushPoints(shf_mounting_hole_points)
            .hole(M5_CLEARANCE_CLOSE_DIAMETER)
        )

    def _make_post_transom(self, height: float):
        """Create transom post."""
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
            .center(0, self.HEIGHT - Vslot2020.WIDTH)
            .cboreHole(
                M5_CLEARANCE_CLOSE_DIAMETER,
                M5_COUNTERBORE_DIAMETER,
                Vslot2020.COUNTERBORE_DEPTH,
                depth=None,
            )
            .tag("hole_deck")
        )

    def make(self):
        """Create assembly."""
        bracket_light_duty = BracketStandardLightDuty90().cq_object
        bracket_standard_duty = BracketStandardStandardDuty90().cq_object

        post = self._make_post(self.POST_HEIGHT)
        post_rocker_axle = self._make_post_rocker_axle(self.POST_HEIGHT)
        post_transom = self._make_post_transom(self.HEIGHT + self.TRANSOM_HEIGHT)

        beam_side_deck = self._make_beam_side(
            self.BEAM_SIDE_LENGTH,
            differential_pivot_beam_offset=self.DIFFERENTIAL_PIVOT_BEAM_OFFSET,
        )
        beam_side_belly = self._make_beam_side(self.BEAM_SIDE_LENGTH)
        beam_end = self._make_beam_end(self.BEAM_END_LENGTH)
        beam_differential_pivot = self._make_beam_differential_pivot(
            self.WIDTH - (2 * Vslot2020.WIDTH)
        )

        # position fore-starboard post
        # rotate to place center bore slot on inside of frame
        # translate in X direction so base is on the XY plane
        post_fore_starboard = post.rotateAboutCenter((0, 0, 1), 180).translate(
            (-self.BEAM_END_LENGTH / 2 - Vslot2020.WIDTH / 2, 0, Vslot2020.WIDTH)
        )
        # rotate beam so counterbore is on opposite side to center bore slot
        beam_side_deck = beam_side_deck.rotateAboutCenter((0, 0, 1), 180)
        beam_side_belly = beam_side_belly.rotateAboutCenter((0, 0, 1), 180)

        assembly = (
            cq.Assembly(color=self.aluminium_anodised_natural)
            .add(
                post_fore_starboard,
                name="post_fore_starboard",
            )
            .add(
                post,
                name="post_fore_port",
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2 + Vslot2020.WIDTH / 2,
                        0,
                        Vslot2020.WIDTH,
                    ),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                post_transom,
                name="post_aft_starboard_transom",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2 - Vslot2020.WIDTH / 2,
                        self.LENGTH + self.TRANSOM_LENGTH - Vslot2020.WIDTH,
                        0,
                    ),
                    cq.Vector(0, 0, 1),
                    90,
                ),
            )
            .add(
                post_transom,
                name="post_aft_port_transom",
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2 + Vslot2020.WIDTH / 2,
                        self.LENGTH + self.TRANSOM_LENGTH - Vslot2020.WIDTH,
                        0,
                    ),
                    cq.Vector(0, 0, 1),
                    90,
                ),
            )
            .add(
                post_rocker_axle,
                name="post_port_rocker_axle",
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2 + Vslot2020.WIDTH / 2,
                        self.ROCKER_AXLE_DISTANCE_FROM_FORE - (Vslot2020.WIDTH / 2),
                        Vslot2020.WIDTH,
                    ),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                post_rocker_axle,
                name="post_starboard_rocker_axle",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2 - Vslot2020.WIDTH / 2,
                        self.ROCKER_AXLE_DISTANCE_FROM_FORE - (Vslot2020.WIDTH / 2),
                        Vslot2020.WIDTH,
                    ),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
            .add(
                beam_side_belly,
                name="beam_starboard_belly",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2 - Vslot2020.WIDTH / 2,
                        -Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(1, 0, 0),
                    -90,
                ),
            )
            .add(
                beam_side_deck,
                name="beam_starboard_deck",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2 - Vslot2020.WIDTH / 2,
                        -Vslot2020.WIDTH / 2,
                        self.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(1, 0, 0),
                    -90,
                ),
            )
            .add(
                beam_side_belly.mirror("ZY"),
                name="beam_port_belly",
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2 + Vslot2020.WIDTH / 2,
                        -Vslot2020.WIDTH / 2,
                        Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(1, 0, 0),
                    -90,
                ),
            )
            .add(
                beam_side_deck.mirror("ZY"),
                name="beam_port_deck",
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2 + Vslot2020.WIDTH / 2,
                        -Vslot2020.WIDTH / 2,
                        self.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(1, 0, 0),
                    -90,
                ),
            )
            .add(
                beam_end,
                name="beam_fore_belly",
                loc=cq.Location(
                    cq.Vector(-self.BEAM_END_LENGTH / 2, 0, Vslot2020.WIDTH / 2),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                beam_end,
                name="beam_fore_deck",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2,
                        0,
                        self.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                beam_end,
                name="beam_aft_deck",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2,
                        self.LENGTH - Vslot2020.WIDTH,
                        self.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                beam_end,
                name="beam_aft_belly",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2,
                        self.LENGTH - Vslot2020.WIDTH,
                        Vslot2020.WIDTH / 2,
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                beam_differential_pivot,
                name="beam_differential_pivot",
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2,
                        self.DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE
                        - (Vslot2020.WIDTH / 2)
                        + self.DIFFERENTIAL_PIVOT_BEAM_OFFSET,
                        self.HEIGHT - (Vslot2020.WIDTH / 2),
                    ),
                    cq.Vector(0, 1, 0),
                    90,
                ),
            )
            .add(
                bracket_standard_duty,
                name="bracket_starboard_beam_differential",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2
                        + BracketStandardStandardDuty90.LENGTH / 2,
                        BracketStandardStandardDuty90.LENGTH / 2
                        + self.DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE
                        + self.DIFFERENTIAL_PIVOT_BEAM_OFFSET,
                        self.HEIGHT - (BracketStandardStandardDuty90.WIDTH / 2),
                    ),
                    cq.Vector(-1, 0, 0),
                    90,
                ),
            )
            .add(
                bracket_standard_duty.mirror("YZ"),
                name="bracket_port_beam_differential",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2
                        - BracketStandardStandardDuty90.LENGTH / 2,
                        BracketStandardStandardDuty90.LENGTH / 2
                        + self.DIFFERENTIAL_PIVOT_DISTANCE_FROM_FORE
                        + self.DIFFERENTIAL_PIVOT_BEAM_OFFSET,
                        self.HEIGHT - (BracketStandardStandardDuty90.WIDTH / 2),
                    ),
                    cq.Vector(-1, 0, 0),
                    90,
                ),
            )
            .add(
                bracket_light_duty,
                name="bracket_starboard_belly",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2
                        + BracketStandardLightDuty90.LENGTH / 2,
                        0,
                        Vslot2020.WIDTH + BracketStandardLightDuty90.LENGTH / 2,
                    )
                ),
            )
            .add(
                bracket_light_duty.mirror("XY"),
                name="bracket_starboard_deck",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        -self.BEAM_END_LENGTH / 2
                        + BracketStandardLightDuty90.LENGTH / 2,
                        0,
                        self.HEIGHT
                        - Vslot2020.WIDTH
                        - BracketStandardLightDuty90.LENGTH / 2,
                    )
                ),
            )
            .add(
                bracket_light_duty.mirror("ZY"),
                name="bracket_port_belly",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2
                        - BracketStandardLightDuty90.LENGTH / 2,
                        0,
                        Vslot2020.WIDTH + BracketStandardLightDuty90.LENGTH / 2,
                    )
                ),
            )
            .add(
                bracket_light_duty,
                name="bracket_port_deck",
                color=self.aluminium_cast,
                loc=cq.Location(
                    cq.Vector(
                        self.BEAM_END_LENGTH / 2
                        - BracketStandardLightDuty90.LENGTH / 2,
                        0,
                        self.HEIGHT
                        - Vslot2020.WIDTH
                        - BracketStandardLightDuty90.LENGTH / 2,
                    ),
                    cq.Vector(0, 1, 0),
                    180,
                ),
            )
        )

        return assembly

    @staticmethod
    def color_assembly(frame):
        """Color frame assembly."""
        color_post = cq.Color("blue")
        color_side_beam = cq.Color("green")
        color_lateral_beam = cq.Color("red")

        frame.objects["post_fore_starboard"].color = color_post
        frame.objects["post_fore_port"].color = color_post
        frame.objects["post_aft_starboard_transom"].color = color_post
        frame.objects["post_aft_port_transom"].color = color_post
        frame.objects["post_port_rocker_axle"].color = color_post
        frame.objects["post_starboard_rocker_axle"].color = color_post

        frame.objects["beam_starboard_belly"].color = color_side_beam
        frame.objects["beam_starboard_deck"].color = color_side_beam
        frame.objects["beam_port_belly"].color = color_side_beam
        frame.objects["beam_port_deck"].color = color_side_beam

        frame.objects["beam_fore_belly"].color = color_lateral_beam
        frame.objects["beam_fore_deck"].color = color_lateral_beam
        frame.objects["beam_aft_deck"].color = color_lateral_beam
        frame.objects["beam_aft_belly"].color = color_lateral_beam
        frame.objects["beam_differential_pivot"].color = color_lateral_beam

        return frame
