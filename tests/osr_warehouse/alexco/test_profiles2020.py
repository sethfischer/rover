"""Aluminium Extrusion Company V-slot extrusion tests."""

import pytest

from osr_warehouse.alexco.profiles20 import Vslot20BoreSlot, Vslot2020Profile

from ...constants import TOLERANCE


class TestVslot20BoreSlot:
    """AEC 20 series bore slot tests."""

    def setup_method(self) -> None:
        """Initialise."""
        bore_slot = Vslot20BoreSlot()
        self.sketch = bore_slot.cq_object
        self.wires = bore_slot._make(assemble=False)

    def test_faces_count(self) -> None:
        """Test number of faces."""
        assert 1 == len(self.sketch._faces.Faces())

    def test_area(self) -> None:
        """Test area."""
        assert pytest.approx(6.224999, TOLERANCE) == self.sketch._faces.Area()

    def test_vertices_count(self) -> None:
        """Test number of vertices."""
        assert 12 == len(self.wires.vertices()._selection)

    def test_bore_slot_width(self) -> None:
        """Test bore slot width."""
        assert 1.5 == self.wires.edges()._selection[0].Length()

    def test_edges_count(self) -> None:
        """Test number of edges."""
        assert 6 == len(self.wires.edges()._selection)


class TestVslot2020ProfileWithoutFillets:
    """AEC 2020 V-slot profile tests."""

    def setup_method(self) -> None:
        """Initialise."""
        profile = Vslot2020Profile()
        self.sketch_without_fillets = profile._make(fillet=False)

    def test_vertices_count(self) -> None:
        """Test number of vertices."""
        assert 85 == len(self.sketch_without_fillets.reset().vertices()._selection)

    def test_tag_bounding_box_vertices(self) -> None:
        """Test tagged bounding box vertices."""
        assert 6 == len(
            self.sketch_without_fillets.reset()
            .vertices(tag="bounding_box_vertices")
            ._selection
        )

    def test_edge_count(self) -> None:
        """Test number of edges."""
        assert 71 == len(self.sketch_without_fillets.reset().edges()._selection)
