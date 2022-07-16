"""Generic V-slot T-nuts for 20 mm series extrusion."""


import cadquery as cq
import cq_warehouse.extensions  # noqa: F401
from cq_warehouse.fastener import SocketHeadCapScrew


class SlidingTNut20:
    """20 mm series V-slot sliding T-nut.

    :param size: Size of threaded hole.
    :type size: string, defaults to "M5-0.8"
    :param length: Length of nut.
    :type length: float
    :param simple: Create shape with reduced detail.
    :type simple: bool, optional, defaults to True
    """

    def __init__(self, size: str = "M5-0.8", length: float = 9.5, simple: bool = True):
        """20 mm series V-slot sliding T-nut."""
        self.size = size
        self.length = length
        self.simple = simple

        self.trapezoid_width = 5.5
        self.trapezoid_height = 3.4
        self.key_width = 6
        self.key_height = 1.5

        self._cq_object = self.make()

    @property
    def cq_object(self) -> cq.Workplane:
        """20 mm series V-slot sliding T-nut."""
        return self._cq_object

    def profile(self) -> cq.Sketch:
        """T-nut profile sketch."""
        profile = (
            cq.Sketch()
            .trapezoid(self.trapezoid_width, self.trapezoid_height, 115)
            .edges(">Y")
            .rect(self.key_width, self.key_height * 2)
            .clean()
            .moved(
                cq.Location(
                    cq.Vector(0, -(self.trapezoid_height / 2 + self.key_height), 0)
                )
            )
        )
        return profile

    def make(self) -> cq.Workplane:
        """Make 20 mm series V-slot sliding T-nut.

        :return: 20 mm series V-slot sliding T-nut.
        :rtype: cadquery.Workplane
        """
        thickness = self.trapezoid_height + self.key_height

        screw = SocketHeadCapScrew(
            size=self.size, fastener_type="iso4762", length=3, simple=self.simple
        )

        result = (
            cq.Workplane("YZ", origin=(-self.length / 2, 0, 0))
            .placeSketch(self.profile())
            .extrude(self.length)
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            # type: ignore[attr-defined]
            .threadedHole(screw, thickness, counterSunk=False, simple=self.simple)
        )

        return result
