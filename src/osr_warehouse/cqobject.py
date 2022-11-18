"""Abstract base classes for CadQuery object containers."""

from abc import ABC, abstractmethod


class CqObjectContainer(ABC):
    """Abstract base class for CadQuery object containers."""

    @property
    @abstractmethod
    def cq_object(self):
        """Get CadQuery object."""
        pass

    @abstractmethod
    def _make(self):
        """Create CadQuery object."""
        pass


class CqAssemblyContainer(CqObjectContainer):
    """Abstract base class for CadQuery assembly object containers."""

    @abstractmethod
    def cq_part(self, name: str):
        """Get part from CadQuery assembly."""
        pass

    @abstractmethod
    def bom_parts(self):
        """Part identifiers for use in bill of materials."""
        pass
