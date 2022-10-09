"""Aluminium Extrusion Company V-slot extrusion tests."""

import pytest

from osr_warehouse.alexco.profiles20 import Vslot20BoreSlot

from ...constants import TOLERANCE


class TestVslot20BoreSlot:
    """AEC 20 series bore slot tests."""

    def setup(self):
        """Initialise fixtures."""
        bore_slot = Vslot20BoreSlot()
        self.sketch = bore_slot.cq_object
        self.wires = bore_slot._make(assemble=False)

    def test_faces_count(self):
        """Test number of faces."""
        assert 1 == len(self.sketch._faces.Faces())

    def test_area(self):
        """Test area."""
        assert pytest.approx(6.224999, TOLERANCE) == self.sketch._faces.Area()

    def test_vertices_count(self):
        """Test number of vertices."""
        assert 12 == len(self.wires.vertices()._selection)

    def test_bore_slot_width(self):
        """Test bore slot width."""
        assert 1.5 == self.wires.edges()._selection[0].Length()

    def test_edges_count(self):
        """Test number of edges."""
        assert 6 == len(self.wires.edges()._selection)
