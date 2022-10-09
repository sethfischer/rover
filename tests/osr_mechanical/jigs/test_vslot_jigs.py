"""V-slot jig tests."""

from osr_mechanical.jigs.vslot import EndTapJig


class TestEndTagJig2020:
    """2020 end tap jig tests."""

    def setup(self):
        """Initialise."""
        self.body_name = "2020_end_tap_jig__body"

    def test_default_body_is_valid(self):
        """Test default end tap jig body is valid."""
        jig = EndTapJig()
        body = jig.cq_part(self.body_name)

        assert body.val().isValid()

    def test_short_body_is_valid(self):
        """Test short end tap jig body is valid."""
        jig = EndTapJig(height=60)
        body = jig.cq_part(self.body_name)

        assert body.val().isValid()

    def test_long_body_is_valid(self):
        """Test long end tap jig body is valid."""
        jig = EndTapJig(height=120)
        body = jig.cq_part(self.body_name)

        assert body.val().isValid()
