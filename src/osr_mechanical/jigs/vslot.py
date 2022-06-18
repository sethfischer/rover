"""V-slot jigs and guides."""

import cadquery as cq


class EndTapJig:
    """V-slot end tap jig.

    :param height: Length of jig.
    :type height: float, optional, defaults to 60
    :param clearance: V-slot fit. A higher value results in a tighter fit.
    :type clearance: float, optional, defaults to 0.15
    """

    TINY_LENGTH = 0.001  # 1μm

    def __init__(self, height: float = 70, clearance: float = 0.15):
        """Initialise V-slot end tap jig."""
        self.height = height
        self.clearance = clearance

        self.thickness = 6

        self.vslot_width = 20
        self.key_width = 6.3
        self.key_depth = 3.5

        self.stop_width = 5
        self.tap_guide_hole_diameter = 5.5

        self.fixing_hole_diameter = 4.5
        self.nut_length = 10
        self.swarf_cavity_depth = 20

        self.width = self.vslot_width + (self.thickness * 2)
        self.swarf_cavity_elevation = self.height - self.thickness
        self.stop_elevation = self.swarf_cavity_elevation - self.swarf_cavity_depth

        self.fixing_hole_elevation = (self.stop_elevation / 2) + (
            (self.height / 2) - self.stop_elevation
        )

        self.nut_retainer_elevation = (
            self.fixing_hole_elevation - ((self.height / 2) - self.stop_elevation)
        ) + (self.nut_length / 2)

    def slot_sketch(self, depth):
        """Sketch to approximate V-slot profile."""
        sketch = (
            cq.Sketch()
            .rect(self.vslot_width, self.vslot_width + self.clearance, tag="base")
            .edges(">Y", tag="base")
            .rect(self.key_width - self.clearance, depth * 2, mode="s", tag="key_right")
            .edges("<Y", tag="base")
            .rect(self.key_width - self.clearance, depth * 2, mode="s", tag="key_left")
            .clean()
        )

        return sketch

    def make(self):
        """Make CadQuery object."""
        sketch_nut_retainer = self.slot_sketch(self.key_depth)

        result = (
            cq.Workplane("XY")
            .box(self.vslot_width, self.width, self.height)
            .faces(">Z")
            .workplane()
            .tag("workplane_aperture_end")
            .workplaneFromTagged("workplane_aperture_end")
            .placeSketch(sketch_nut_retainer)
            .cutBlind(-self.stop_elevation)
            .workplaneFromTagged("workplane_aperture_end")
            .rect(self.vslot_width, self.vslot_width - (2 * self.stop_width))
            .cutBlind(-self.swarf_cavity_elevation)
            .faces("<Z")
            .workplane()
            .tag("workplane_aperture_end")
            .hole(self.tap_guide_hole_diameter)
            .faces(">Z")
            .workplane(offset=-self.nut_retainer_elevation)
            .rect(self.vslot_width, self.vslot_width + self.clearance)
            .cutBlind(self.nut_length)
            .faces("<Y")
            .workplane(centerOption="CenterOfBoundBox")
            .center(0, self.fixing_hole_elevation)
            .hole(self.fixing_hole_diameter)
            .edges("|X")
            .edges("<<Y[-3] or >>Y[-3]")
            .edges("<<Z[1]")
            .chamfer(1.75 * self.key_depth, self.key_depth - self.TINY_LENGTH)
            .edges("|Y")
            .edges(">>Z[3]")
            .chamfer(self.key_width / 5)
            .edges(">Z")
            .edges("not(<Y or >Y or <X or >X)")
            # An asymmetric .chamfer(2.5, 4) would be preferred.
            # See https://github.com/CadQuery/cadquery/issues/786
            .chamfer(2.5)
        )

        return result
