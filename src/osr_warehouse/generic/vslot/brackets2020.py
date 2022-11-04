"""Generic V-slot brackets for 2020 extrusion."""

import cadquery as cq

from osr_warehouse.cqobject import CqObjectContainer


class StandardLightDuty90(CqObjectContainer):
    """Standard light duty 90° angle bracket.

    Two-rib light-duty 90° angle bracket for V-slot aluminium extrusion.

    :Manufacturer: Generic
    """

    LENGTH = WIDTH = 20
    THICKNESS = 3
    HOLE_DIAMETER = 5.5

    _description = "T-slot standard light-duty 90° angle bracket: {}×{}mm."

    def __init__(self) -> None:
        """Initialise bracket."""
        self._cq_object = self._make()

    @property
    def description(self) -> str:
        """Object description."""
        return self._description.format(self.LENGTH, self.WIDTH)

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    def _make(self) -> cq.Workplane:
        """Make standard light duty 90° angle bracket."""
        profile_inverse = (
            cq.Sketch()
            .segment((0, 0), (-self.LENGTH + self.THICKNESS, 0))
            .segment((0, -self.LENGTH + self.THICKNESS))
            .close()
            .assemble()
        )

        bracket = (
            cq.Workplane()
            .box(self.LENGTH, self.WIDTH, self.LENGTH)
            .faces("+Z or +X")
            .shell(-self.THICKNESS)
            .faces("<X")
            .workplane()
            .hole(self.HOLE_DIAMETER)
            .faces("<Z")
            .workplane(centerOption="CenterOfMass")
            .hole(self.HOLE_DIAMETER)
            .faces("<Y")
            .vertices(">XZ")
            .workplane(centerOption="CenterOfMass")
            .placeSketch(profile_inverse)
            .extrude("last", combine="s")
            .edges("%LINE")
            .fillet(1)
        )

        return bracket


class StandardStandardDuty90(CqObjectContainer):
    """Standard standard-duty 90° angle bracket.

    Two-rib standard-duty 90° angle bracket for V-slot aluminium extrusion.

    :Manufacturer: Generic
    """

    LENGTH = 30
    WIDTH = 20
    THICKNESS = 3
    HOLE_DIAMETER = 5.5

    _description = "T-slot standard standard-duty 90° angle bracket: {}×{}mm."

    def __init__(self) -> None:
        """Initialise dimensions."""
        self.brace_step_length = 0.1 * self.LENGTH
        self.brace_step_height = 0.1 * self.LENGTH

        self._cq_object = self._make()

    @property
    def description(self) -> str:
        """Object description."""
        return self._description.format(self.LENGTH, self.WIDTH)

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    def _make(self) -> cq.Workplane:
        """Make standard standard-duty 90° angle bracket."""
        profile_inverse = (
            cq.Sketch()
            .segment(
                (0, 0), (0, -self.LENGTH + self.THICKNESS + self.brace_step_height)
            )
            .segment(
                (
                    -self.THICKNESS - self.brace_step_length,
                    -self.LENGTH + self.THICKNESS + self.brace_step_height,
                )
            )
            .segment(
                (
                    -self.LENGTH + self.THICKNESS + self.brace_step_height,
                    -self.THICKNESS - self.brace_step_length,
                )
            )
            .segment((-self.LENGTH + self.THICKNESS + self.brace_step_height, 0))
            .close()
            .assemble()
        )

        result = (
            cq.Workplane()
            .box(self.LENGTH, self.WIDTH, self.LENGTH)
            .faces("+Z or +X")
            .shell(-self.THICKNESS)
            .faces("<X")
            .workplane()
            .hole(self.HOLE_DIAMETER)
            .faces("<Z")
            .workplane(centerOption="CenterOfMass")
            .hole(self.HOLE_DIAMETER)
            .faces("<Y")
            .vertices(">XZ")
            .workplane(centerOption="CenterOfMass")
            .placeSketch(profile_inverse)
            .extrude("last", combine="s")
            .edges("%LINE")
            .fillet(1)
        )

        return result
