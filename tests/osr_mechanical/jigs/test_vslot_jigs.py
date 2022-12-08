"""V-slot jig tests."""

from cadquery import Shape, Workplane

from osr_mechanical.jigs.vslot import EndTapJig


class TestEndTagJig2020:
    """2020 end tap jig tests."""

    def setup_method(self) -> None:
        """Set up TestEndTagJig2020."""
        self.body_name = "2020_end_tap_jig__body"

    def test_default_body_is_valid(self) -> None:
        """Test default end tap jig body is valid."""
        jig = EndTapJig()
        body = jig.cq_part(self.body_name)

        assert isinstance(body, Workplane)
        shape = body.val()
        assert isinstance(shape, Shape)

        assert shape.isValid()

    def test_short_body_is_valid(self) -> None:
        """Test short end tap jig body is valid."""
        jig = EndTapJig(height=60)
        body = jig.cq_part(self.body_name)

        assert isinstance(body, Workplane)
        shape = body.val()
        assert isinstance(shape, Shape)

        assert shape.isValid()

    def test_long_body_is_valid(self) -> None:
        """Test long end tap jig body is valid."""
        jig = EndTapJig(height=120)
        body = jig.cq_part(self.body_name)

        assert isinstance(body, Workplane)
        shape = body.val()
        assert isinstance(shape, Shape)

        assert shape.isValid()
