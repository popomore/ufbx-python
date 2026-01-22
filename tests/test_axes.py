"""
Tests for CoordinateAxis, CoordinateAxes, and Scene.axes
"""

import os

import pytest

import ufbx


def test_coordinate_axis_enum():
    """CoordinateAxis has all 7 values matching ufbx C API."""
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_POSITIVE_X")
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_NEGATIVE_X")
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_POSITIVE_Y")
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_NEGATIVE_Y")
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_POSITIVE_Z")
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_NEGATIVE_Z")
    assert hasattr(ufbx.CoordinateAxis, "COORDINATE_AXIS_UNKNOWN")

    assert ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_X == 0
    assert ufbx.CoordinateAxis.COORDINATE_AXIS_NEGATIVE_X == 1
    assert ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_Y == 2
    assert ufbx.CoordinateAxis.COORDINATE_AXIS_NEGATIVE_Y == 3
    assert ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_Z == 4
    assert ufbx.CoordinateAxis.COORDINATE_AXIS_NEGATIVE_Z == 5
    assert ufbx.CoordinateAxis.COORDINATE_AXIS_UNKNOWN == 6

    assert isinstance(ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_X, int)


def test_coordinate_axes():
    """CoordinateAxes construction, .right/.up/.front, clamping, __repr__."""
    from ufbx._ufbx import CoordinateAxes

    ax = CoordinateAxes(0, 2, 4)
    assert ax.right == ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_X
    assert ax.up == ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_Y
    assert ax.front == ufbx.CoordinateAxis.COORDINATE_AXIS_POSITIVE_Z

    ax2 = CoordinateAxes(1, 3, 5)
    assert ax2.right == ufbx.CoordinateAxis.COORDINATE_AXIS_NEGATIVE_X
    assert ax2.up == ufbx.CoordinateAxis.COORDINATE_AXIS_NEGATIVE_Y
    assert ax2.front == ufbx.CoordinateAxis.COORDINATE_AXIS_NEGATIVE_Z

    # Out-of-range -> UNKNOWN
    ax3 = CoordinateAxes(99, -1, 7)
    assert ax3.right == ufbx.CoordinateAxis.COORDINATE_AXIS_UNKNOWN
    assert ax3.up == ufbx.CoordinateAxis.COORDINATE_AXIS_UNKNOWN
    assert ax3.front == ufbx.CoordinateAxis.COORDINATE_AXIS_UNKNOWN

    assert "CoordinateAxes" in repr(ax)
    assert "right=" in repr(ax) and "up=" in repr(ax) and "front=" in repr(ax)


def test_scene_has_axes_property():
    """Scene exposes axes property."""
    assert hasattr(ufbx.Scene, "axes")


@pytest.fixture
def fbx_path():
    p = os.path.join(os.path.dirname(__file__), "fixtures", "maya_cube.fbx")
    return p if os.path.exists(p) else None


def test_scene_axes(fbx_path):
    """Scene.axes returns CoordinateAxes with right/up/front as CoordinateAxis."""
    if fbx_path is None:
        pytest.skip("maya_cube.fbx not found (see tests/fixtures/README.md)")

    with ufbx.load_file(fbx_path) as scene:
        ax = scene.axes
        assert ax is not None
        assert hasattr(ax, "right") and hasattr(ax, "up") and hasattr(ax, "front")
        assert isinstance(ax.right, ufbx.CoordinateAxis)
        assert isinstance(ax.up, ufbx.CoordinateAxis)
        assert isinstance(ax.front, ufbx.CoordinateAxis)
        assert "CoordinateAxes" in repr(ax)


def test_scene_axes_after_close(fbx_path):
    """Accessing axes after scene.close() raises RuntimeError."""
    if fbx_path is None:
        pytest.skip("maya_cube.fbx not found (see tests/fixtures/README.md)")

    scene = ufbx.load_file(fbx_path)
    scene.close()
    with pytest.raises(RuntimeError, match="closed"):
        _ = scene.axes
