"""V-slot jigs and guides."""

import cadquery as cq
import cq_warehouse.extensions  # noqa: F401
from cq_warehouse.fastener import PlainWasher, SocketHeadCapScrew

from osr_warehouse.generic.vslot.tnut20 import SlidingTNut20
from osr_warehouse.utilities import MetricBoltSpecification


class EndTapJig:
    """V-slot end tap jig.

    :param height: Length of jig.
    :type height: float, optional, defaults to 60
    :param clearance: V-slot fit. A higher value results in a tighter fit.
    :type clearance: float, optional, defaults to 0.15
    """

    TINY_LENGTH = 0.001  # 1μm

    def __init__(
        self, height: float = 70, clearance: float = 0.15, simple: bool = True
    ):
        """Initialise V-slot end tap jig."""
        self.height = height
        self.clearance = clearance
        self.simple = simple

        self.thickness = 6

        self.vslot_width = 20
        self.key_width = 6.3
        self.key_depth = 3.5

        self.stop_width = 5
        self.tap_guide_hole_diameter = 5.5

        self.tslot_nut_length = 10
        self.swarf_cavity_depth = 20

        bolt_spec = MetricBoltSpecification(5, 0.8, 12)

        self.width = None
        self.swarf_cavity_elevation = None
        self.stop_elevation = None
        self.fixing_hole_elevation = None
        self.nut_retainer_elevation = None

        self.tslot_nut = None
        self.screw = None
        self.washer = None

        self._calculate_dimensions()
        self._make_fasteners(bolt_spec)

        self._assembly = self.make()

    def _calculate_dimensions(self):
        """Calculate derived dimensions."""
        self.width = self.vslot_width + (self.thickness * 2)
        self.swarf_cavity_elevation = self.height - self.thickness
        self.stop_elevation = self.swarf_cavity_elevation - self.swarf_cavity_depth

        self.fixing_hole_elevation = (self.stop_elevation / 2) + (
            (self.height / 2) - self.stop_elevation
        )

        self.nut_retainer_elevation = (
            self.fixing_hole_elevation - ((self.height / 2) - self.stop_elevation)
        ) + (self.tslot_nut_length / 2)

    def _make_fasteners(self, bolt_spec: MetricBoltSpecification) -> None:
        """Make fasteners."""
        self.tslot_nut = (
            SlidingTNut20(bolt_spec.specification(), simple=self.simple)
            .cq_object.rotateAboutCenter((0, 1, 0), -90)
            .rotateAboutCenter((0, 0, 1), 90)
            .translate((0, -7.5, 15.2))
        )

        self.screw = SocketHeadCapScrew(
            size=bolt_spec.specification(),
            fastener_type="iso4762",
            length=bolt_spec.length,
            simple=self.simple,
        )

        self.washer = PlainWasher(size=bolt_spec.shaft_m, fastener_type="iso7093")

    def slot_sketch(self, depth) -> cq.Sketch:
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

    @property
    def body(self) -> cq.Workplane:
        """Jig body."""
        return self._assembly.objects["body"].obj

    @property
    def assembly(self) -> cq.Assembly:
        """Jig assembly."""
        return self._assembly

    def make(self) -> cq.Assembly:
        """Make jig body and assembly."""
        assembly = cq.Assembly(None, name="2020-end-tap-jig")

        sketch_nut_retainer = self.slot_sketch(self.key_depth)

        body = (
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
            .cutBlind(self.tslot_nut_length)
            .faces("<Y")
            .workplane(centerOption="CenterOfBoundBox")
            .center(0, self.fixing_hole_elevation)
            .clearanceHole(
                self.screw,
                washers=[self.washer],
                counterSunk=False,
                baseAssembly=assembly,
            )
            .faces(">Y")
            .workplane(centerOption="CenterOfBoundBox")
            .center(0, self.fixing_hole_elevation)
            .clearanceHole(
                self.screw,
                washers=[self.washer],
                counterSunk=False,
                baseAssembly=assembly,
            )
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

        assembly.add(body, name="body", color=cq.Color("goldenrod2"))
        assembly.add(self.tslot_nut, name="tslot_nut_left")
        assembly.add(self.tslot_nut.mirror("ZX"), name="tslot_nut_right")

        return assembly
