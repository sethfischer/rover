"""Tests for OSR mechanical design."""

from osr_warehouse.point2d import Point2D


class TestPoint2D:
    """Test Point2D."""

    def test_construct_no_param(self) -> None:
        """Create Point2D."""
        result = Point2D()

        assert result.x == 0
        assert result.y == 0

    def test_construct_with_x(self) -> None:
        """Create Point2D with x coordinate."""
        result = Point2D(x=1)

        assert result == (1, 0)

    def test_construct_with_y(self) -> None:
        """Create Point2D with x coordinate."""
        result = Point2D(y=1)

        assert result == (0, 1)

    def test_get_x(self) -> None:
        """Get x coordinate."""
        result = Point2D(x=1)

        assert result == (1, 0)

    def test_get_y(self) -> None:
        """Get y coordinate."""
        result = Point2D(y=1)

        assert result == (0, 1)

    def test_reflect_x(self) -> None:
        """Reflect point in x-axis."""
        point = Point2D(x=1, y=2)
        result = point.reflect_x()

        assert point == (1, 2)
        assert result == (1, -2)

    def test_reflect_y(self) -> None:
        """Reflect point in y-axis."""
        point = Point2D(x=1, y=2)
        result = point.reflect_y()

        assert point == (1, 2)
        assert result == (-1, 2)

    def test_reflect_y_with_x_offset(self) -> None:
        """Reflect point in y-axis."""
        point = Point2D(x=1, y=2)
        result = point.reflect_y(x_offset=1)

        assert point == (1, 2)
        assert result == (1, 2)

    def test_reflect_xy(self) -> None:
        """Reflect point in axis x=y."""
        point = Point2D(x=1, y=2)
        result = point.reflect_xy()

        assert point == (1, 2)
        assert result == (2, 1)

    def test_reflect_xy_with_x_offset(self) -> None:
        """Reflect point in axis x=y with x offset."""
        point = Point2D(x=1, y=2)
        result = point.reflect_xy(x_offset=2)

        assert point == (1, 2)
        assert result == (4, -1)

    def test_reflect_xy_neg(self) -> None:
        """Reflect point in axis negative x=y."""
        point = Point2D(x=1, y=2)
        result = point.reflect_xy()

        assert point == (1, 2)
        assert result == (2, 1)

    def test_translate_x(self) -> None:
        """Translate a point in the x-direction."""
        point = Point2D(x=1, y=2)
        result = point.translate_x(2)

        assert point == (1, 2)
        assert result == (3, 2)

    def test_repr(self) -> None:
        """String representation."""
        result = Point2D(x=1, y=2)

        assert str(result) == "Point2D(1, 2)"
