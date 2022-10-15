"""Aluminium Extrusion Company 20-series profiles.

`Aluminium Extrusion Company <https://www.alexco.co.nz/>`_.
"""

from math import radians, sqrt, tan
from typing import Union

import cadquery as cq

from osr_warehouse.cqobject import CqObjectContainer
from osr_warehouse.point2d import Point2D


class Vslot20BoreSlot(CqObjectContainer):
    """Bore slot for AEC 20-series V-slot Aluminium Extrusion.

    Consists of a channel and a groove.
    """

    def __init__(self, mirror: bool = False, x_offset: Union[float, int] = 0) -> None:
        """Initialise dimensions."""
        self.mirror = mirror
        self.x_offset = x_offset

        if mirror:
            self.x_offset = -x_offset

        self.core_x_pos_intersect = Point2D(self.x_offset, 0)
        self.core_channel_vertex_q2 = Point2D(
            x_offset,
            Vslot2020Profile.HALF_BORE_CHANNEL_WIDTH,
        )
        self.channel_groove_vertex = Point2D(
            Vslot2020Profile.BORE_CHANNEL_DEPTH + self.x_offset,
            Vslot2020Profile.HALF_BORE_CHANNEL_WIDTH,
        )
        self.bore_groove_depth = Vslot2020Profile.HALF_BORE_CHANNEL_WIDTH * tan(
            radians(Vslot2020Profile.BORE_GROOVE_ANGLE_OBTUSE)
        )
        self.bore_groove_vertex = Point2D(
            Vslot2020Profile.BORE_CHANNEL_DEPTH
            + self.bore_groove_depth
            + self.x_offset,
            0,
        )

        if mirror:
            self.core_x_pos_intersect = self.core_x_pos_intersect.reflect_y()
            self.channel_groove_vertex = self.channel_groove_vertex.reflect_y()
            self.bore_groove_vertex = self.bore_groove_vertex.reflect_y()

        self._cq_object = self._make()

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    def _make(self, assemble=True):
        """Create bore slot sketch."""
        sketch = (
            cq.Sketch()
            .segment(self.core_x_pos_intersect, self.core_channel_vertex_q2)
            .segment(self.channel_groove_vertex)
            .segment(self.bore_groove_vertex)
            .segment(self.channel_groove_vertex.reflect_x())
            .segment(self.core_channel_vertex_q2.reflect_x())
            .close()
        )

        if assemble:
            sketch = sketch.assemble()

        return sketch


class Vslot2020Profile(CqObjectContainer):
    """2020 V-slot Aluminium Extrusion profile.

    :Manufacturer: Aluminium Extrusion Company
    :Web: https://www.alexco.co.nz/
    :Part: AEC 2020
    """

    WIDTH = 20
    CORE_WIDTH = 8
    RIB_THICKNESS = 1.6627
    SLOT_WIDTH = 10.9
    SLOT_CHAMFER = 2.62
    SLOT_DEPTH = 4.3
    CENTER_BORE_DIAMETER = 4.2
    HALF_BETWEEN_V_LOWER_VERTICES = 2.7

    BORE_CHANNEL_WIDTH = 3
    BORE_CHANNEL_DEPTH = 1.325
    BORE_GROOVE_ANGLE_OBTUSE = 45

    HALF_BORE_CHANNEL_WIDTH = BORE_CHANNEL_WIDTH / 2

    def __init__(self) -> None:
        """Initialise dimensions."""
        self.half_width = self.WIDTH / 2
        self.half_core_width = self.CORE_WIDTH / 2
        self.half_rib_thickness = self.RIB_THICKNESS / 2
        self.half_slot_width = self.SLOT_WIDTH / 2
        self.center_bore_radius = self.CENTER_BORE_DIAMETER / 2

        self.core_x_pos_intersect = Point2D(self.half_core_width, 0)
        self.core_rib_vertex_y = self.half_core_width - sqrt(
            self.half_rib_thickness**2 + self.half_rib_thickness**2
        )
        self.core_rib_vertex = Point2D(self.half_core_width, self.core_rib_vertex_y)
        self.rib_wall_vertex_x = self.half_core_width + self.SLOT_CHAMFER
        self.rib_slot_vertex = Point2D(self.rib_wall_vertex_x, self.half_slot_width)
        self.slot_retainer_vertex = Point2D(
            self.half_core_width + self.SLOT_DEPTH,
            self.half_slot_width,
        )
        self.v_lower_vertex = Point2D(
            self.slot_retainer_vertex.x,
            self.half_slot_width - self.HALF_BETWEEN_V_LOWER_VERTICES,
        )
        self.v_upper_vertex = Point2D(
            self.half_width,
            (self.half_width - self.v_lower_vertex.x) + self.v_lower_vertex.y,
        )

        self._cq_object = self._make()

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    def _make(self, fillet: bool = True):
        """Create profile."""
        result = self._make_main_sketch()

        sketch_bore_slot = Vslot20BoreSlot(x_offset=-self.half_core_width).cq_object
        result = result.face(sketch_bore_slot, mode="s")

        result = self._make_center_lines(result)
        result = self._tag_vertices(result)

        if fillet:
            result = self._fillet(result)

        return result

    def _make_main_sketch(self):
        """Create main profile."""
        result = (
            cq.Sketch()
            .parray(0, 0, 360, 4)
            # quadrant 1
            .segment(self.core_x_pos_intersect, self.core_rib_vertex)
            .segment(self.rib_slot_vertex)
            .segment(self.slot_retainer_vertex)
            .segment(self.v_lower_vertex)
            .segment(self.v_upper_vertex)
            .segment((self.half_width, self.half_width))
            .segment(self.v_upper_vertex.reflect_xy())
            .segment(self.v_lower_vertex.reflect_xy())
            .segment(self.slot_retainer_vertex.reflect_xy())
            .segment(self.rib_slot_vertex.reflect_xy())
            .segment(self.core_rib_vertex.reflect_xy())
            .segment((0, self.half_core_width))
            .segment((0, 0))
            .close()
            .assemble()
            .clean()
        )

        result = result.reset().circle(self.center_bore_radius, mode="s")

        return result

    def _make_center_lines(self, profile):
        """Create center lines."""
        points = [
            (self.half_core_width, 0),
            (0, self.half_core_width),
            (0, -self.half_core_width),
        ]
        result = profile.reset().push(points).circle(0.25, mode="s")

        return result

    def _tag_vertices(self, profile):
        """Tag all vertices."""
        profile = self._tag_vertices_centerbore_groove(profile)
        profile = self._tag_vertices_bounding_box(profile)
        profile = self._tag_vertices_slot_retainer(profile)
        profile = self._tag_vertices_v_lower(profile)
        profile = self._tag_vertices_v_upper(profile)
        profile = self._tag_vertices_rib_slot(profile)
        profile = self._tag_vertices_core_rib(profile)
        profile = self._tag_vertices_core_channel(profile)
        profile = self._tag_vertices_channel_groove(profile)
        profile = self._tag_vertices_cline(profile)

        return profile

    @staticmethod
    def _tag_vertices_centerbore_groove(profile):
        """Tag centerbore grove."""
        return profile.reset().vertices(">>X[9]").tag("centerbore_groove_vertices")

    @staticmethod
    def _tag_vertices_bounding_box(profile):
        """Tag bounding box vertices."""
        result = (
            profile.reset()
            .vertices("(>X and <Y) or (>X and >Y) or (<X and <Y) or (<X and >Y)")
            .tag("bounding_box_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_slot_retainer(profile):
        """Tag slot retainer."""
        selector = {
            "q1": "(>>Y[1] and >>X[3]) or (>>X[1] and >>Y[3])",
            "q2": "(<<Y[1] and >>X[3]) or (>>X[1] and <<Y[3])",
            "q3": "(<<Y[3] and <<X[1]) or (<<Y[1] and <<X[3])",
            "q4": "(>>Y[3] and <<X[1]) or (>>Y[1] and <<X[3])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("slot_retainer_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_v_lower(profile):
        """Tag V-slot lower vertices."""
        selector = {
            "q1": "(<<X[1] and <<Y[7]) or (<<X[7] and <<Y[1])",
            "q2": "(>>X[1] and <<Y[7]) or (>>X[7] and <<Y[1])",
            "q3": "(>>X[1] and >>Y[7]) or (>>X[7] and >>Y[1])",
            "q4": "(<<X[1] and >>Y[7]) or (<<X[7] and >>Y[1])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("v_lower_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_v_upper(profile):
        """Tag V-slot upper vertices."""
        selector = {
            "q1": "(<<X[0] and <<Y[4]) or (<<X[4] and <<Y[0])",
            "q2": "(>>X[0] and <<Y[4]) or (>>X[4] and <<Y[0])",
            "q3": "(>>X[0] and >>Y[4]) or (>>X[4] and >>Y[0])",
            "q4": "(<<X[0] and >>Y[4]) or (<<X[4] and >>Y[0])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("v_upper_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_rib_slot(profile):
        """Tag rib slot vertices."""
        result = (
            profile.reset()
            .vertices("<<X[2] or >>X[2] or <<Y[2] or >>Y[2]")
            .tag("rib_slot_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_core_rib(profile):
        """Tag core rib vertices."""
        selector = {
            "q1": "(<<X[5] and <<Y[6]) or (<<X[6] and <<Y[5])",
            "q2": "(>>X[5] and <<Y[6]) or (>>X[6] and <<Y[5])",
            "q3": "(>>X[5] and >>Y[6]) or (>>X[6] and >>Y[5])",
            "q4": "(<<X[5] and >>Y[6]) or (<<X[6] and >>Y[5])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("core_rib_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_core_channel(profile):
        """Tag core channel vertices."""
        result = (
            profile.reset()
            .vertices("(>>X[5] and <<Y[8]) or (>>X[5] and >>Y[8])")
            .tag("core_channel_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_channel_groove(profile):
        """Tag channel groove vertices."""
        return profile.reset().vertices(">>X[8]").tag("channel_groove_vertices")

    @staticmethod
    def _tag_vertices_cline(profile):
        """Tag center line vertices."""
        selector = {
            "positive_x": "(<<X[5] and <<Y[12]) or (<<X[5] and >>Y[12])",
            "positive_y": "(<<X[11] and <<Y[5]) or (<<X[9] and <<Y[5])",
            "negative_y": "(<<X[11] and >>Y[5]) or (<<X[9] and >>Y[5])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("cline_vertices")
        )

        return result

    @staticmethod
    def _fillet(profile):
        """Fillet vertices."""
        profile.vertices(tag="centerbore_groove_vertices").fillet(0.3)
        profile.vertices(tag="bounding_box_vertices").fillet(0.5)
        profile.vertices(tag="slot_retainer_vertices").fillet(0.25)
        profile.vertices(tag="v_lower_vertices").fillet(0.25)
        profile.vertices(tag="v_upper_vertices").fillet(0.3)
        profile.vertices(tag="rib_slot_vertices").fillet(0.3)
        profile.vertices(tag="core_rib_vertices").fillet(0.3)
        profile.vertices(tag="core_channel_vertices").fillet(0.3)
        profile.vertices(tag="channel_groove_vertices").fillet(0.3)
        profile.vertices(tag="cline_vertices").fillet(0.3)

        return profile


class Vslot2040Profile(CqObjectContainer):
    """2040 V-slot Aluminium Extrusion profile.

    :Manufacturer: Aluminium Extrusion Company
    :Web: https://www.alexco.co.nz/
    :Part: AEC 2040
    """

    def __init__(self) -> None:
        """Initialise dimensions."""
        self.aec_2020 = Vslot2020Profile()

        # Quadrant 1 is a partial copy of Vslot2020Profile.
        self.q1_core_rib_vertex = self.aec_2020.core_rib_vertex.translate_x(
            self.aec_2020.half_width
        )
        self.q1a_rib_slot_vertex = self.aec_2020.rib_slot_vertex.translate_x(
            self.aec_2020.half_width
        )
        self.q1a_slot_retainer_vertex = self.aec_2020.slot_retainer_vertex.translate_x(
            self.aec_2020.half_width
        )
        self.q1a_v_lower_vertex = self.aec_2020.v_lower_vertex.translate_x(
            self.aec_2020.half_width
        )
        self.q1a_v_upper_vertex = self.aec_2020.v_upper_vertex.translate_x(
            self.aec_2020.half_width
        )
        self.q1a_bounding_box_vertex = Point2D(
            self.aec_2020.half_width, self.aec_2020.half_width
        ).translate_x(self.aec_2020.half_width)

        self.q1aprime_v_upper_vertex = self.q1a_v_upper_vertex.reflect_xy(
            x_offset=self.aec_2020.half_width
        )
        self.q1aprime_v_lower_vertex = self.q1a_v_lower_vertex.reflect_xy(
            x_offset=self.aec_2020.half_width
        )
        self.q1aprime_slot_retainer_vertex = self.q1a_slot_retainer_vertex.reflect_xy(
            x_offset=self.aec_2020.half_width
        )
        self.q1aprime_rib_slot_vertex = self.q1a_rib_slot_vertex.reflect_xy(
            x_offset=self.aec_2020.half_width
        )
        self.q1aprime_core_rib_vertex = self.q1_core_rib_vertex.reflect_xy(
            x_offset=self.aec_2020.half_width
        )

        self.q1b_core_rib_vertex = self.q1aprime_core_rib_vertex.reflect_y(
            x_offset=self.aec_2020.half_width
        )
        self.q1b_rib_slot_vertex = self.q1aprime_rib_slot_vertex.reflect_y(
            x_offset=self.aec_2020.half_width
        )
        self.q1b_slot_retainer_vertex = self.q1aprime_slot_retainer_vertex.reflect_y(
            x_offset=self.aec_2020.half_width
        )
        self.q1b_v_lower_vertex = self.q1aprime_v_lower_vertex.reflect_y(
            x_offset=self.aec_2020.half_width
        )
        self.q1b_v_upper_vertex = self.q1aprime_v_upper_vertex.reflect_y(
            x_offset=self.aec_2020.half_width
        )

        self._cq_object = self._make()

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    def _make(self):
        """Make profile."""
        profile = self._make_main_sketch()

        sketch_center_cavity = self._make_center_cavity_sketch()
        profile = profile.face(sketch_center_cavity, mode="s")

        profile = self._make_center_bore(profile)

        sketch_bore_slot_q1and4 = Vslot20BoreSlot(
            x_offset=-(Vslot2020Profile.WIDTH / 2 + Vslot2020Profile.CORE_WIDTH / 2)
        ).cq_object
        profile = profile.reset().face(sketch_bore_slot_q1and4, mode="s")

        sketch_bore_slot_q2and3 = Vslot20BoreSlot(
            x_offset=Vslot2020Profile.WIDTH / 2 + Vslot2020Profile.CORE_WIDTH / 2,
            mirror=True,
        ).cq_object
        profile = profile.reset().face(sketch_bore_slot_q2and3, mode="s")

        profile = self._make_center_lines(profile)
        profile = self._tag_vertices(profile)
        profile = self._fillet(profile)

        return profile

    def _make_main_sketch(self):
        result = (
            cq.Sketch()
            # quadrant 1
            .segment(self.q1_core_rib_vertex, self.q1a_rib_slot_vertex)
            .segment(self.q1a_slot_retainer_vertex)
            .segment(self.q1a_v_lower_vertex)
            .segment(self.q1a_v_upper_vertex)
            .segment(self.q1a_bounding_box_vertex)
            .segment(self.q1aprime_v_upper_vertex)
            .segment(self.q1aprime_v_lower_vertex)
            .segment(self.q1aprime_slot_retainer_vertex)
            .segment(self.q1aprime_rib_slot_vertex)
            .segment(self.q1aprime_core_rib_vertex)
            .segment(self.q1b_core_rib_vertex)
            .segment(self.q1b_rib_slot_vertex)
            .segment(self.q1b_slot_retainer_vertex)
            .segment(self.q1b_v_lower_vertex)
            .segment(self.q1b_v_upper_vertex)
            # quadrant 2
            .segment(self.q1b_v_upper_vertex.reflect_y())
            .segment(self.q1b_v_lower_vertex.reflect_y())
            .segment(self.q1b_slot_retainer_vertex.reflect_y())
            .segment(self.q1b_rib_slot_vertex.reflect_y())
            .segment(self.q1b_core_rib_vertex.reflect_y())
            .segment(self.q1aprime_core_rib_vertex.reflect_y())
            .segment(self.q1aprime_rib_slot_vertex.reflect_y())
            .segment(self.q1aprime_slot_retainer_vertex.reflect_y())
            .segment(self.q1aprime_v_lower_vertex.reflect_y())
            .segment(self.q1aprime_v_upper_vertex.reflect_y())
            .segment(self.q1a_bounding_box_vertex.reflect_y())
            .segment(self.q1a_v_upper_vertex.reflect_y())
            .segment(self.q1a_v_lower_vertex.reflect_y())
            .segment(self.q1a_slot_retainer_vertex.reflect_y())
            .segment(self.q1a_rib_slot_vertex.reflect_y())
            .segment(self.q1_core_rib_vertex.reflect_y())
            # quadrant 3
            .segment(self.q1_core_rib_vertex.reflect_xy_neg())
            .segment(self.q1a_rib_slot_vertex.reflect_xy_neg())
            .segment(self.q1a_slot_retainer_vertex.reflect_xy_neg())
            .segment(self.q1a_v_lower_vertex.reflect_xy_neg())
            .segment(self.q1a_v_upper_vertex.reflect_xy_neg())
            .segment(self.q1a_bounding_box_vertex.reflect_xy_neg())
            .segment(self.q1aprime_v_upper_vertex.reflect_xy_neg())
            .segment(self.q1aprime_v_lower_vertex.reflect_xy_neg())
            .segment(self.q1aprime_slot_retainer_vertex.reflect_xy_neg())
            .segment(self.q1aprime_rib_slot_vertex.reflect_xy_neg())
            .segment(self.q1aprime_core_rib_vertex.reflect_xy_neg())
            .segment(self.q1b_core_rib_vertex.reflect_xy_neg())
            .segment(self.q1b_rib_slot_vertex.reflect_xy_neg())
            .segment(self.q1b_slot_retainer_vertex.reflect_xy_neg())
            .segment(self.q1b_v_lower_vertex.reflect_xy_neg())
            .segment(self.q1b_v_upper_vertex.reflect_xy_neg())
            # quadrant 4
            .segment(self.q1b_v_upper_vertex.reflect_x())
            .segment(self.q1b_v_lower_vertex.reflect_x())
            .segment(self.q1b_slot_retainer_vertex.reflect_x())
            .segment(self.q1b_rib_slot_vertex.reflect_x())
            .segment(self.q1b_core_rib_vertex.reflect_x())
            .segment(self.q1aprime_core_rib_vertex.reflect_x())
            .segment(self.q1aprime_rib_slot_vertex.reflect_x())
            .segment(self.q1aprime_slot_retainer_vertex.reflect_x())
            .segment(self.q1aprime_v_lower_vertex.reflect_x())
            .segment(self.q1aprime_v_upper_vertex.reflect_x())
            .segment(self.q1a_bounding_box_vertex.reflect_x())
            .segment(self.q1a_v_upper_vertex.reflect_x())
            .segment(self.q1a_v_lower_vertex.reflect_x())
            .segment(self.q1a_slot_retainer_vertex.reflect_x())
            .segment(self.q1a_rib_slot_vertex.reflect_x())
            .segment(self.q1_core_rib_vertex.reflect_x())
            .close()
            .assemble()
            .clean()
        )

        return result

    @staticmethod
    def _make_center_cavity_sketch():
        """Create center cavity sketch."""
        major_radius = 6
        minor_radius = 2

        result = (
            cq.Sketch()
            .circle(major_radius)
            .push([(0, major_radius), (0, -major_radius)])
            .circle(minor_radius, mode="a")
            .clean()
            .reset()
            .vertices()
            .fillet(3.25)
        )

        return result

    def _make_center_bore(self, profile):
        """Create center bore."""
        result = (
            profile.reset()
            .push(
                [
                    (self.aec_2020.half_width, 0),
                    (-self.aec_2020.half_width, 0),
                ]
            )
            .circle(self.aec_2020.center_bore_radius, mode="s")
        )

        return result

    def _make_center_lines(self, profile):
        """Create center lines."""
        points = [
            (self.aec_2020.half_width, self.aec_2020.half_core_width),
            (self.aec_2020.half_width, -self.aec_2020.half_core_width),
            (-self.aec_2020.half_width, self.aec_2020.half_core_width),
            (-self.aec_2020.half_width, -self.aec_2020.half_core_width),
        ]

        return profile.reset().push(points).circle(0.25, mode="s")

    def _tag_vertices(self, profile):
        """Tag all vertices."""
        profile = self._tag_vertices_centerbore_groove(profile)
        profile = self._tag_vertices_bounding_box(profile)
        profile = self._tag_vertices_slot_retainer(profile)
        profile = self._tag_vertices_v_lower(profile)
        profile = self._tag_vertices_v_upper(profile)
        profile = self._tag_vertices_rib_slot(profile)
        profile = self._tag_vertices_core_rib(profile)
        profile = self._tag_vertices_core_channel(profile)
        profile = self._tag_vertices_channel_groove(profile)
        profile = self._tag_vertices_cline(profile)

        return profile

    @staticmethod
    def _tag_vertices_centerbore_groove(profile):
        """Tag centerbore grove."""
        return (
            profile.reset()
            .vertices(">>X[9] or <<X[9]")
            .tag("centerbore_groove_vertices")
        )

    @staticmethod
    def _tag_vertices_bounding_box(profile):
        """Tag bounding box vertices."""
        return (
            profile.reset()
            .vertices("(>X and <Y) or (>X and >Y) or (<X and <Y) or (<X and >Y)")
            .tag("bounding_box_vertices")
        )

    @staticmethod
    def _tag_vertices_slot_retainer(profile):
        """Tag slot retainer."""
        selector = {
            "q1": "(<<X[1] and <<Y[4]) or (<<X[3] and <<Y[1]) or (<<X[15] and <<Y[1])",
            "q2": "(>>X[1] and <<Y[4]) or (>>X[3] and <<Y[1]) or (>>X[16] and <<Y[1])",
            "q3": "(>>X[1] and >>Y[4]) or (>>X[3] and >>Y[1] or (>>X[16] and >>Y[1]))",
            "q4": "(<<X[1] and >>Y[4]) or (<<X[3] and >>Y[1]) or (<<X[15] and >>Y[1])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("slot_retainer_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_v_lower(profile):
        """Tag V-slot lower vertices."""
        selector = {
            "q1": "(<<X[7] and <<Y[1]) or (<<X[12] and <<Y[1]) or (<<X[1] and <<Y[9])",
            "q2": "(>>X[7] and <<Y[1]) or (>>X[13] and <<Y[1]) or (>>X[1] and <<Y[9])",
            "q3": "(>>X[7] and >>Y[1]) or (>>X[13] and >>Y[1]) or (>>X[1] and >>Y[9])",
            "q4": "(<<X[7] and >>Y[1]) or (<<X[12] and >>Y[1]) or (<<X[1] and >>Y[9])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("v_lower_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_v_upper(profile):
        """Tag V-slot upper vertices."""
        selector = {
            "q1": "(<<X[4] and <<Y[0]) or (<<X[0] and <<Y[6]) or (<<X[14] and <<Y[0])",
            "q2": "(>>X[4] and <<Y[0]) or (>>X[0] and <<Y[6]) or (>>X[15] and <<Y[0])",
            "q3": "(>>X[4] and >>Y[0]) or (>>X[0] and >>Y[6]) or (>>X[15] and >>Y[0])",
            "q4": "(<<X[4] and >>Y[0]) or (<<X[0] and >>Y[6]) or (<<X[14] and >>Y[0])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("v_upper_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_rib_slot(profile):
        """Tag rib slot vertices."""
        result = (
            profile.reset()
            .vertices("<<X[2] or >>X[2] or <<Y[3] or >>Y[3]")
            .tag("rib_slot_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_core_rib(profile):
        """Tag core rib vertices."""
        selector = {
            "q1": "(<<X[5] and <<Y[8]) or (<<X[6] and <<Y[7]) or (<<X[13] and <<Y[7])",
            "q2": "(>>X[5] and <<Y[8]) or (>>X[6] and <<Y[7]) or (>>X[14] and <<Y[7])",
            "q3": "(>>X[5] and >>Y[8]) or (>>X[6] and >>Y[7]) or (>>X[14] and >>Y[7])",
            "q4": "(<<X[5] and >>Y[8]) or (<<X[6] and >>Y[7]) or (<<X[13] and >>Y[7])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("core_rib_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_core_channel(profile):
        """Tag core channel vertices."""
        selector = {
            "q1": "(<<X[5] and <<Y[10])",
            "q2": "(>>X[5] and <<Y[10])",
            "q3": "(>>X[5] and >>Y[10])",
            "q4": "(<<X[5] and >>Y[10])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("core_channel_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_channel_groove(profile):
        """Tag channel groove vertices."""
        result = (
            profile.reset().vertices("<<X[8] or >>X[8]").tag("channel_groove_vertices")
        )

        return result

    @staticmethod
    def _tag_vertices_cline(profile):
        """Tag center line vertices."""
        selector = {
            "q1": "(<<X[10] and <<Y[7]) or (<<X[11] and <<Y[7])",
            "q2": "(>>X[10] and <<Y[7]) or (>>X[11] and <<Y[7])",
            "q3": "(>>X[10] and >>Y[7]) or (>>X[11] and >>Y[7])",
            "q4": "(<<X[10] and >>Y[7]) or (<<X[11] and >>Y[7])",
        }
        result = (
            profile.reset()
            .vertices(" or ".join(selector.values()))
            .tag("cline_vertices")
        )

        return result

    @staticmethod
    def _fillet(profile):
        """Fillet vertices."""
        profile.vertices(tag="centerbore_groove_vertices").fillet(0.3)
        profile.vertices(tag="bounding_box_vertices").fillet(0.5)
        profile.vertices(tag="slot_retainer_vertices").fillet(0.25)
        profile.vertices(tag="v_lower_vertices").fillet(0.25)
        profile.vertices(tag="v_upper_vertices").fillet(0.3)
        profile.vertices(tag="rib_slot_vertices").fillet(0.3)
        profile.vertices(tag="core_rib_vertices").fillet(0.3)
        profile.vertices(tag="core_channel_vertices").fillet(0.3)
        profile.vertices(tag="channel_groove_vertices").fillet(0.3)
        profile.vertices(tag="cline_vertices").fillet(0.3)

        return profile
