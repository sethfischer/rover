"""Describes cartesian coordinates for 2D points."""

from __future__ import annotations

from typing import NamedTuple


class Point2D(NamedTuple):
    """Describes cartesian coordinates for 2D points."""

    x: float = 0
    y: float = 0

    def reflect_x(self) -> Point2D:
        """Reflect point in the x-axis."""
        return Point2D._make([self.x, -self.y])

    def reflect_y(self, x_offset: float = 0) -> Point2D:
        """Reflect point in the y-axis."""
        if x_offset == 0:
            return Point2D._make([-self.x, self.y])
        else:
            return Point2D._make([-self.x + (x_offset * 2), self.y])

    def reflect_xy(self, x_offset: float = 0) -> Point2D:
        """Reflect point in axis x=y."""
        point = Point2D._make([self.y, self.x])
        if x_offset != 0:
            point = Point2D._make([point.x + x_offset, point.y - x_offset])

        return point

    def reflect_xy_neg(self) -> Point2D:
        """Reflect point in axis negative x=y."""
        return Point2D._make([-self.x, -self.y])

    def translate_x(self, x_offset: float) -> Point2D:
        """Translate a point in the x-direction."""
        return Point2D._make([self.x + x_offset, self.y])

    def __repr__(self) -> str:
        """Return a string with the format 'Point2D(x, y)'."""
        return "Point2D({}, {})".format(self.x, self.y)
