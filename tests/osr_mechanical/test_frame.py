"""Final assembly tests."""

import pytest

from osr_mechanical.frame.final import Frame

from ..constants import TOLERANCE


class TestFrameAssembly:
    """Frame assembly tests."""

    def setup_method(self) -> None:
        """Initialise."""
        self.frame_compound = Frame().cq_object.toCompound()

    def test_bounding_box(self) -> None:
        """Test frame assembly bounding box dimensions."""
        assert pytest.approx(285, TOLERANCE) == self.frame_compound.BoundingBox().xlen
        assert pytest.approx(487, TOLERANCE) == self.frame_compound.BoundingBox().ylen
        assert pytest.approx(190, TOLERANCE) == self.frame_compound.BoundingBox().zlen
