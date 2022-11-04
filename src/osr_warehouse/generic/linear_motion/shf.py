"""SHF series shaft supports."""

from dataclasses import dataclass
from math import radians, sin, tan
from typing import Any

import cadquery as cq

from osr_warehouse.cqobject import CqObjectContainer
from osr_warehouse.point2d import Point2D
from osr_warehouse.utilities import TINY_LENGTH


@dataclass
class SHFDimensions:
    """SHF shaft support dimension schema."""

    length: float
    thickness: float
    flange_thickness: float
    height: float
    collar_diameter: float
    between_mounting_holes: float
    mounting_hole_diameter: float
    shaft_bolt_cylinder_diameter: float
    step_diameter: float
    step_depth: float
    shaft_bolt_cylinder_length: float
    slit_width: float
    to_shaft_bolt_centerline: float
    shaft_bolt_m: float
    shaft_bolt_length: float
    cutout_depth: float
    fillet_radius: float


@dataclass
class SHFSeriesDimensions:
    """SHF shaft support dimensions."""

    shf8: SHFDimensions = SHFDimensions(
        length=43,
        thickness=10,
        flange_thickness=5,
        height=24,
        collar_diameter=20,
        between_mounting_holes=32,
        mounting_hole_diameter=5.5,
        shaft_bolt_cylinder_diameter=9,
        step_diameter=10,
        step_depth=1.5,
        shaft_bolt_cylinder_length=18,
        slit_width=2,
        to_shaft_bolt_centerline=9.5,
        shaft_bolt_m=4,
        shaft_bolt_length=20,
        cutout_depth=0.25,
        fillet_radius=0.5,
    )


class SHF(CqObjectContainer):
    """SHF shaft support.

    Shaft Support - Flanged Slit (Cast Type) - Standard
    """

    FLANGE_ANGLE = 22.5
    _description = "SHF{} shaft support: flanged slit (cast type), standard type."

    def __init__(self, shaft_diameter: int) -> None:
        """
        Initialise SHF shaft support.

        :param shaft_diameter: Nominal shaft diameter (D)
        :type shaft_diameter: int
        """
        self.shaft_diameter = shaft_diameter

        dimensions = getattr(SHFSeriesDimensions, "shf{}".format(shaft_diameter))

        self.length = dimensions.length

        self.thickness = dimensions.thickness
        self.flange_thickness = dimensions.flange_thickness
        self.height = dimensions.height
        self.collar_diameter = dimensions.collar_diameter
        self.between_mounting_holes = dimensions.between_mounting_holes
        self.mounting_hole_diameter = dimensions.mounting_hole_diameter
        self.shaft_bolt_cylinder_diameter = dimensions.shaft_bolt_cylinder_diameter
        self.step_diameter = dimensions.step_diameter
        self.step_depth = dimensions.step_depth
        self.shaft_bolt_cylinder_length = dimensions.shaft_bolt_cylinder_length
        self.slit_width = dimensions.slit_width
        self.to_shaft_bolt_centerline = dimensions.to_shaft_bolt_centerline
        self.shaft_bolt_m = dimensions.shaft_bolt_m
        self.shaft_bolt_length = dimensions.shaft_bolt_length
        self.cutout_depth = dimensions.cutout_depth
        self.fillet_radius = dimensions.fillet_radius

        self._cq_object = self._make()

    @property
    def description(self) -> str:
        """Object description."""
        return self._description.format(self.shaft_diameter)

    @property
    def cq_object(self) -> Any:
        """Get CadQuery object."""
        return self._cq_object.val()

    def _make(self) -> cq.Workplane:
        """Make SHF shaft support."""
        flange_sketch = self._make_flange_sketch()

        result = (
            cq.Workplane()
            # flange
            .placeSketch(flange_sketch)
            .extrude(self.flange_thickness)
            # mounting holes
            .faces(">Z")
            .workplane()
            .tag("workplane_flange")
            .pushPoints(
                [
                    (self.between_mounting_holes / 2, 0),
                    (-self.between_mounting_holes / 2, 0),
                ]
            )
            .hole(self.mounting_hole_diameter)
            # collar
            .workplaneFromTagged("workplane_flange")
            .circle((self.collar_diameter / 2) - TINY_LENGTH)
            .extrude(self.thickness - self.flange_thickness)
            # shaft hole
            .faces(">Z")
            .workplane()
            .tag("workplane_top")
            .hole(self.shaft_diameter)
            # shaft hole step
            .workplaneFromTagged("workplane_top")
            .hole(self.step_diameter, self.step_depth)
        )

        shaft_bolt_cylinder = (
            cq.Workplane("YZ").tag("retainer").center(9.5, 5).cylinder(18, 9 / 2)
        )
        result = result.union(shaft_bolt_cylinder)

        shaft_bolt_hole = cq.Workplane("YZ").center(9.5, 5).cylinder(18, 2)
        result = result.cut(shaft_bolt_hole)

        slot = cq.Workplane().box(2, 20, 10, centered=(True, False, False))
        result = result.cut(slot)

        bolt_cutout_offset = self.length / 2
        bolt_cutout = (
            cq.Workplane("YZ")
            .workplane(offset=bolt_cutout_offset)
            .center(self.to_shaft_bolt_centerline, 5)
            .circle(self.shaft_bolt_cylinder_diameter / 2)
            .extrude(
                -self.length / 2
                + self.shaft_bolt_cylinder_length / 2
                - self.cutout_depth
            )
        )
        result = result.cut(bolt_cutout)

        bolt_cutout_q2 = bolt_cutout.mirror("YZ")
        result = result.cut(bolt_cutout_q2)

        return result.combine()

    def _make_flange_sketch(self) -> Any:
        """Flange sketch."""
        y_pos_intersect = self._calculate_y_pos_intersect(
            self.collar_diameter, self.FLANGE_ANGLE
        )
        q1_vertex = self._calculate_flange_q1_vertex(
            y_pos_intersect, self.length, self.FLANGE_ANGLE
        )

        result = (
            cq.Sketch()
            .segment(y_pos_intersect, q1_vertex)
            .segment(q1_vertex.reflect_x())
            .segment(y_pos_intersect.reflect_x())
            .segment(q1_vertex.reflect_xy_neg())
            .segment(q1_vertex.reflect_y())
            .close()
            .assemble()
            .vertices(">Y or <Y")
            .fillet(self.collar_diameter / 2)
            .reset()
            .vertices(">X or <X")
            .fillet(self.fillet_radius)
            .clean()
        )

        return result

    @staticmethod
    def _calculate_y_pos_intersect(
        collar_diameter: float, flange_angle: float
    ) -> Point2D:
        """Calculate flange positive Y-axis intersection."""
        y = (collar_diameter / 2) / sin(radians(90 - flange_angle))

        return Point2D(x=0, y=y)

    @staticmethod
    def _calculate_flange_q1_vertex(
        y_vertex: Point2D, length: float, flange_angle: float
    ) -> Point2D:
        """Calculate flange vertex in quadrant 1."""
        x = length / 2
        delta = (length / 2) * tan(radians(flange_angle))
        y = y_vertex.y - delta
        return Point2D(x=x, y=y)
