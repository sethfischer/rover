"""SHF shaft support tests."""

from osr_warehouse.generic.linear_motion.shf import SHF


class TestSHF8:
    """SHF shaft support tests."""

    def setup(self) -> None:
        """Initialise fixtures."""
        self.shf8 = SHF(8).cq_object

    def test_is_valid(self) -> None:
        """Test object is valid."""
        assert self.shf8.val().isValid()
