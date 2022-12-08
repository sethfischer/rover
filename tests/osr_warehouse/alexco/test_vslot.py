"""Aluminium Extrusion Company V-slot extrusion tests."""

import pytest

from osr_warehouse.alexco.vslot import Vslot2020, Vslot2040

from ...constants import TOLERANCE


class TestVslot2020:
    """AEC 2020 V-slot extrusion tests."""

    def setup_method(self) -> None:
        """Set up TestVslot2020."""
        factory = Vslot2020()
        self.length = 50
        self.extrusion = factory.make(length=self.length)

    def test_bounding_box(self) -> None:
        """Test extrusion bounding box dimensions."""
        assert pytest.approx(20, TOLERANCE) == self.extrusion.val().BoundingBox().xlen
        assert pytest.approx(20, TOLERANCE) == self.extrusion.val().BoundingBox().ylen
        assert pytest.approx(50, TOLERANCE) == self.extrusion.val().BoundingBox().zlen


class TestVslot2040:
    """AEC 2040 V-slot extrusion tests."""

    def setup_method(self) -> None:
        """Set up TestVslot2040."""
        factory = Vslot2040()
        self.length = 50
        self.extrusion = factory.make(length=self.length)

    def test_bounding_box(self) -> None:
        """Test extrusion bounding box dimensions."""
        assert pytest.approx(40, TOLERANCE) == self.extrusion.val().BoundingBox().xlen
        assert pytest.approx(20, TOLERANCE) == self.extrusion.val().BoundingBox().ylen
        assert pytest.approx(50, TOLERANCE) == self.extrusion.val().BoundingBox().zlen
