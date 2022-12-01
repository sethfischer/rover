"""Rocker axle tests."""

from osr_mechanical.rocker_axle import RockerAxle


class TestRockerAxleAssembly:
    """Rocker axle tests."""

    def setup(self) -> None:
        """Initialise."""
        self.rocker_axle_compound = RockerAxle().cq_object.toCompound()

    def test_is_valid(self) -> None:
        """Test assembly is valid."""
        assert self.rocker_axle_compound.isValid()
