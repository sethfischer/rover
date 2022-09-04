"""Utilities."""

from osr_warehouse.typing import Point

X = 0
Y = 1


def reflect_xy(point: Point, x_offset: float = 0) -> Point:
    """Reflect point in axis x=y.

    Reflect by reversing tuple.
    """
    _point = point[::-1]
    if x_offset != 0:
        _point = (_point[X] + x_offset, _point[Y] - x_offset)

    return _point


def reflect_xy_neg(point: Point) -> Point:
    """Reflect point in axis negative x=y.

    Reflect by reversing tuple.
    """
    return -point[X], -point[Y]


def reflect_x(point: Point) -> Point:
    """Reflect point in the x-axis."""
    return point[X], point[Y] * -1


def reflect_y(point: Point, x_offset: float = 0) -> Point:
    """Reflect point in the y-axis."""
    if x_offset == 0:
        return -point[X], point[Y]
    else:
        return -point[X] + (x_offset * 2), point[Y]


def translate_x(point: Point, x_offset: float) -> Point:
    """Translate a point in the x-direction."""
    return point[X] + x_offset, point[Y]
