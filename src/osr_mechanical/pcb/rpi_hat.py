"""Raspberry Pi HAT mechanical design."""

import cadquery as cq

from osr_common.cq_containers import CqWorkplaneContainer


class RpiHatBoard(CqWorkplaneContainer):
    """Raspberry Pi HAT+ board outline.

    See https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf
    """

    def __init__(self, mounting_holes: bool = True) -> None:
        """Initialise RPi HAT+ board."""
        self.mounting_holes = mounting_holes

        self.width = 65
        self.height = 56.5
        self.thickness = 1.5
        self.corner_radius = 3.5

        self.csi_slot_width = 17
        self.csi_slot_height = 2

        self.dsi_slot_height = 17
        self.dsi_slot_width = 5

        self.mounting_hole_radius = 2.7 / 2
        self.mounting_hole_between_centers_x = 58
        self.mounting_hole_between_centers_y = 49

        dsi_slot_loc_x = -self.width / 2 + self.dsi_slot_width / 2
        dsi_slot_offset_y = -0.5
        self.dsi_slot_loc = (dsi_slot_loc_x, dsi_slot_offset_y)

        self._cq_object = self._make()

    def outline(self) -> cq.Sketch:
        """Create RPi HAT+ board outline."""
        sketch = (
            cq.Sketch()
            .rect(self.width, self.height)
            .vertices()
            .tag("major_outline")
            .push([self.dsi_slot_loc])
            .rect(self.dsi_slot_width, self.dsi_slot_height, mode="s")
            .reset()
            .vertices("(<X and <<Y[2]) or (<X and >>Y[2]) or (<<X[-2])")
            .tag("dsi_slot_vertices")
        )

        if self.mounting_holes:
            sketch.reset().rarray(
                self.mounting_hole_between_centers_x,
                self.mounting_hole_between_centers_y,
                2,
                2,
            ).circle(self.mounting_hole_radius, mode="s")

        sketch.vertices(tag="major_outline").fillet(self.corner_radius)
        sketch.vertices(tag="dsi_slot_vertices").fillet(1)

        return sketch

    def _make(self) -> cq.Workplane:
        """Create RPi HAT+ board."""
        result = (
            cq.Workplane("XY")
            .placeSketch(self.outline())
            .extrude(self.thickness)
            .pushPoints([(-(self.width / 2) + 50, -(self.height / 2) + 11.5)])
            .slot2D(self.csi_slot_width, self.csi_slot_height, angle=90)
            .cutThruAll()
        )

        return result

    def board_face(self) -> cq.Workplane:
        """Face of board.

        For converting to DXF outline.
        """
        return self._cq_object.faces("<Z")
