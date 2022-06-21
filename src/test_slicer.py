from geometry import Slice
from Geometry3D import Point, ConvexPolygon

def test_tool_rect_angle():

    polygon = ConvexPolygon((
        Point(5.0, 0.0, 0.0), Point(5.0, 0.0, 10.0), Point(0.0, 0.0, 5.0)
    ))

    result = Slice._tool_angle({}, polygon)

    assert result == (0, -90.0, 90.0)

def test_tool_sguinch_angle():

    polygon = ConvexPolygon((
        Point(5.0, -1.0, 0.0), Point(5.0, 0.0, 10.0), Point(0.0, 0.0, 5.0)
    ))

    result = Slice._tool_angle({}, polygon)

    assert result == (-45.0, -84.28940686250037, 95.71059313749964)   