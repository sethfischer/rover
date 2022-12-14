"""V-slot jigs and guides."""

from __future__ import annotations

import cadquery as cq
import cq_warehouse.extensions  # noqa: F401
from cq_warehouse.fastener import PlainWasher, SocketHeadCapScrew

from osr_common.cq_containers import CqAssemblyContainer
from osr_common.exceptions import CadQueryTypeError
from osr_mechanical.bom.bom import Bom
from osr_mechanical.bom.parts import Commodity, PartIdentifier, PartTypes
from osr_warehouse.fasteners import MetricBoltSpecification as BoltSpec
from osr_warehouse.generic.vslot.tnut20 import SlidingTNut20
from osr_warehouse.utilities import TINY_LENGTH


class EndTapJig(CqAssemblyContainer):
    """V-slot end tap jig.

    :param height: Length of jig.
    :type height: float, optional, defaults to 60
    :param clearance: Manufacturing compensation. A higher value results in a tighter
        fit.
    :type clearance: float, optional, defaults to 0.15
    :param simple: Create shapes with reduced detail.
    :type simple: bool, optional, defaults to True
    """

    def __init__(
        self, height: float = 70, clearance: float = 0.15, simple: bool = True
    ):
        """Initialise EndTapJig."""
        self.height = height
        self.clearance = clearance
        self.simple = simple

        self._name = "2020_end_tap_jig"

        self.thickness = 6

        self.vslot_width = 20
        self.key_width = 6.3
        self.key_depth = 3.5

        self.stop_width = 5
        self.tap_guide_hole_diameter = 5.5

        self.tslot_nut_length = 10
        self.swarf_cavity_depth = 20

        self.width = self.vslot_width + (self.thickness * 2)
        self.swarf_cavity_elevation = self.height - self.thickness
        self.stop_elevation = self.swarf_cavity_elevation - self.swarf_cavity_depth
        self.fixing_hole_elevation = (
            self.stop_elevation / 2 + self.height / 2 - self.stop_elevation
        )
        self.nut_retainer_elevation = (
            self.fixing_hole_elevation
            - ((height / 2) - self.stop_elevation)
            + self.tslot_nut_length / 2
        )

        bolt_spec = BoltSpec(5, 0.8, 12)
        self.tslot_nut = SlidingTNut20(bolt_spec.specification(), simple=self.simple)
        self.screw = self._make_screw(bolt_spec, self.simple)
        self.washer = self._make_washer(bolt_spec)

        self._cq_object = self._make()

    @staticmethod
    def _make_screw(bolt_spec: BoltSpec, simple: bool = True) -> SocketHeadCapScrew:
        """Make retaining screw."""
        return SocketHeadCapScrew(
            size=bolt_spec.specification(),
            fastener_type="iso4762",
            length=bolt_spec.length,
            simple=simple,
        )

    @staticmethod
    def _make_washer(bolt_spec: BoltSpec) -> PlainWasher:
        """Make retaining screw washer."""
        return PlainWasher(size=bolt_spec.shaft_m, fastener_type="iso7093")

    def slot_sketch(self, depth: float) -> cq.Sketch:
        """Sketch to approximate V-slot profile."""
        return (
            cq.Sketch()
            .rect(self.vslot_width, self.vslot_width + self.clearance, tag="base")
            .edges(">Y", tag="base")
            .rect(self.key_width - self.clearance, depth * 2, mode="s", tag="key_right")
            .edges("<Y", tag="base")
            .rect(self.key_width - self.clearance, depth * 2, mode="s", tag="key_left")
            .clean()
        )

    def _make(self) -> cq.Assembly:
        """Make jig assembly."""
        tslot_nut = (
            self.tslot_nut.cq_object.rotate((0, -1, 0), (0, 1, 0), -90)
            .rotate((0, 0, -1), (0, 0, 1), -90)
            .translate((0, self.vslot_width / 2, self.fixing_hole_elevation))
        )

        assembly = cq.Assembly(
            name=self.name,
            metadata={Bom.PARTS_KEY: self.part_identifiers()},
        )

        body = self._make_body(assembly)

        assembly.add(
            body,
            name=self.sub_assembly_name("body"),
            color=cq.Color("goldenrod2"),
        )
        assembly.add(
            tslot_nut,
            name=self.sub_assembly_name("tslot_nut_left"),
        )
        assembly.add(
            tslot_nut.mirror("ZX"),
            name=self.sub_assembly_name("tslot_nut_right"),
        )

        return assembly

    def _make_body(self, assembly: cq.Assembly) -> cq.Workplane:
        """Make jig body."""
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
            .cutBlind(self.tslot_nut_length)
            .faces("<Y")
            .workplane(centerOption="CenterOfBoundBox")
            .center(0, self.fixing_hole_elevation)
            .clearanceHole(  # type: ignore[attr-defined]
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
            .chamfer(1.75 * self.key_depth, self.key_depth - TINY_LENGTH)
            .edges("|Y")
            .edges(">>Z[3]")
            .chamfer(self.key_width / 5)
            .edges(">Z")
            .edges("not(<Y or >Y or <X or >X)")
            # An asymmetric .chamfer(2.5, 4) would be preferred.
            # See https://github.com/CadQuery/cadquery/issues/786
            .chamfer(2.5)
        )

        if not isinstance(result, cq.Workplane):
            raise CadQueryTypeError(cq.Workplane, result)

        return result

    def part_identifiers(self) -> dict[str, PartIdentifier]:
        """Part identifiers for use in bill of materials."""
        body = PartIdentifier(
            PartTypes.additive,
            "JIG-ENDTAP",
            "3D printed body for end-tap jig. To fit 20 series T-slot extrusion.",
            Commodity.FABRICATED,
        )
        tslot_nut = PartIdentifier(
            PartTypes.tslot, "NUT-M5", self.tslot_nut.description
        )

        return {
            self.sub_assembly_name("body"): body,
            self.sub_assembly_name("tslot_nut_left"): tslot_nut,
            self.sub_assembly_name("tslot_nut_right"): tslot_nut,
        }
