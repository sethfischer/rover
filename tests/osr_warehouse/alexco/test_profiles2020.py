"""Aluminium Extrusion Company V-slot extrusion tests."""

import pytest

from osr_warehouse.alexco.profiles20 import Vslot20BoreSlot, Vslot2020Profile

from ...constants import TOLERANCE


class TestVslot20BoreSlot:
    """AEC 20 series bore slot tests."""

    def setup_method(self) -> None:
        """Set up TestVslot20BoreSlot."""
        bore_slot = Vslot20BoreSlot()
        self.sketch = bore_slot.cq_object

    def test_faces_count(self) -> None:
        """Test number of faces."""
        assert 1 == len(self.sketch.faces().vals())

    def test_area(self) -> None:
        """Test area."""
        assert pytest.approx(6.224999, TOLERANCE) == self.sketch._faces.Area()

    def test_vertices_count(self) -> None:
        """Test number of vertices."""
        assert 18 == len(self.sketch.vertices().vals())

    def test_bore_slot_width(self) -> None:
        """Test bore slot width."""
        assert 1.5 == self.sketch.edges().vals()[0].Length()

    def test_edges_count(self) -> None:
        """Test number of edges."""
        assert 6 == len(self.sketch.faces().edges().vals())


class TestVslot2020ProfileWithoutFillets:
    """AEC 2020 V-slot profile tests."""

    def setup_method(self) -> None:
        """Set up TestVslot2020ProfileWithoutFillets."""
        profile = Vslot2020Profile()
        self.sketch_without_fillets = profile._make(fillet=False)

    def test_vertices_count(self) -> None:
        """Test number of vertices."""
        self.sketch_without_fillets.reset()
        assert 85 == len(self.sketch_without_fillets.vertices().vals())

    def test_tag_bounding_box_vertices(self) -> None:
        """Test tagged bounding box vertices."""
        self.sketch_without_fillets.reset()
        assert 6 == len(
            self.sketch_without_fillets.vertices(tag="bounding_box_vertices").vals()
        )

    def test_edge_count(self) -> None:
        """Test number of edges."""
        self.sketch_without_fillets.reset()
        assert 71 == len(self.sketch_without_fillets.edges().vals())
