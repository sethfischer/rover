"""Abstract base classes for CadQuery object containers."""

from __future__ import annotations

from abc import ABC, abstractmethod

import cadquery as cq


class CqObjectContainer(ABC):
    """Abstract base class for CadQuery object containers."""

    _cq_object: cq.Shape | cq.Sketch | cq.Workplane | cq.Assembly

    @property
    def cq_object(self):
        """Get CadQuery object."""
        return self._cq_object

    @abstractmethod
    def _make(self):
        """Create CadQuery object."""
        ...
