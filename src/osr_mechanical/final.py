"""Final assembly."""

import cadquery as cq

from osr_mechanical.frame import Frame
from osr_warehouse.cqobject import CqAssemblyContainer


class FinalAssembly(CqAssemblyContainer):
    """Final assembly."""

    def __init__(self, simple: bool = False):
        """Initialise final assembly."""
        self.simple = simple

        self.frame = Frame(simple=self.simple)

        self._cq_object = self.make()

    def cq_part(self, name: str):
        """Get part from CadQuery assembly."""
        result = self._cq_object.objects[name].obj
        if result is None:
            raise Exception("Part is not a valid Shape or Workplane.")

        return result

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    def make(self):
        """Make assembly."""
        assembly = cq.Assembly().add(self.frame.cq_object, name="frame")

        return assembly
