"""Raspberry Pi HAT mechanical design."""

import cadquery as cq

from osr_common.cq_containers import CqWorkplaneContainer


class RpiHatBoard(CqWorkplaneContainer):
    """Raspberry Pi HAT+ board outline.

    Reference
    ---------

    * `Raspberry Pi HAT+ Specification <https://datasheets.raspberrypi.com/hat/hat-plus-specification.pdf>`__
    * `Raspberry Pi 3b plus mechanical drawing <https://datasheets.raspberrypi.com/rpi3/raspberry-pi-3-b-plus-mechanical-drawing.pdf>`__
    """  # noqa: E501

    def __init__(self, mounting_holes: bool = True, full_size: bool = True) -> None:
        """Initialise RPi HAT+ board."""
        self.mounting_holes = mounting_holes

        self.full_size = full_size

        self.full_width = 85
        self.standard_width = 65

        self.height = 56.5
        self.thickness = 1.5
        self.corner_radius = 3.5

        self.csi_slot_width = 17
        self.csi_slot_height = 2
        self.csi_slot_location = (45, 11.5)

        self.dsi_slot_height = 17
        self.dsi_slot_width = 5
        self.dsi_slot_location = (self.dsi_slot_width / 2, 28)

        self.mounting_hole_radius = 2.75 / 2
        mounting_hole_from_edge = 3.5
        mounting_hole_between_centers_x = 58
        mounting_hole_between_centers_y = 49

        self.mounting_hole_locations = [
            (mounting_hole_from_edge, mounting_hole_from_edge),
            (
                mounting_hole_from_edge,
                mounting_hole_between_centers_y + mounting_hole_from_edge,
            ),
            (
                mounting_hole_between_centers_x + mounting_hole_from_edge,
                mounting_hole_from_edge + mounting_hole_between_centers_y,
            ),
            (
                mounting_hole_from_edge + mounting_hole_between_centers_x,
                mounting_hole_from_edge,
            ),
        ]

        self._cq_object = self._make()

    def outline(self, width: float) -> cq.Sketch:
        """HAT pcb outline."""
        sketch = (
            cq.Sketch()
            .push([(width / 2, self.height / 2)])
            .rect(width, self.height)
            .reset()
            .vertices()
            .tag("major_vertices")
            .push([self.dsi_slot_location])
            .rect(self.dsi_slot_width, self.dsi_slot_height, mode="s")
            .reset()
            .vertices("(<X and <<Y[2]) or (<X and >>Y[2]) or (<<X[-2])")
            .tag("dsi_notch_vertices")
        )

        sketch.vertices(tag="major_vertices").fillet(self.corner_radius)
        sketch.vertices(tag="dsi_notch_vertices").fillet(1)

        if self.mounting_holes:
            (
                sketch.reset()
                .push(self.mounting_hole_locations)
                .circle(self.mounting_hole_radius, mode="s")
            )

        return sketch

    def _make(self) -> cq.Workplane:
        """Create RPi HAT+ board."""
        if self.full_size:
            width = self.full_width
        else:
            width = self.standard_width

        outline = self.outline(width)

        result = (
            cq.Workplane("XY")
            .placeSketch(outline)
            .extrude(self.thickness)
            .pushPoints([self.csi_slot_location])
            .slot2D(self.csi_slot_width, self.csi_slot_height, angle=90)
            .cutThruAll()
        )

        return result

    def board_face(self) -> cq.Workplane:
        """Face of board.

        For converting to DXF outline.
        """
        return self._cq_object.faces("<Z")
