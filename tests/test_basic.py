"""
Basic Functionality Tests
"""

import pytest

import ufbx


def test_version():
    """Test version number"""
    assert ufbx.__version__ == '0.0.0'


def test_imports():
    """Test that all public APIs can be imported"""
    assert hasattr(ufbx, 'Scene')
    assert hasattr(ufbx, 'load_file')
    assert hasattr(ufbx, 'load_memory')
    assert hasattr(ufbx, 'UfbxError')
    assert hasattr(ufbx, 'UfbxFileNotFoundError')
    assert hasattr(ufbx, 'RotationOrder')


def test_file_not_found():
    """Test that exception is raised when file does not exist"""
    with pytest.raises(ufbx.UfbxFileNotFoundError) as exc_info:
        ufbx.load_file('nonexistent_file.fbx')

    assert 'nonexistent_file.fbx' in str(exc_info.value)


def test_rotation_order_enum():
    """Test enum type"""
    assert ufbx.RotationOrder.ROTATION_ORDER_XYZ.value >= 0
    assert ufbx.RotationOrder.ROTATION_ORDER_XZY.value >= 0

    # Enum should be integer
    assert isinstance(ufbx.RotationOrder.ROTATION_ORDER_XYZ.value, int)


def test_scene_class():
    """Test basic properties of Scene class"""
    # Scene should have load_file class method
    assert hasattr(ufbx.Scene, 'load_file')
    assert hasattr(ufbx.Scene, 'load_memory')

    # Should not directly construct Scene
    # (Can construct, but requires passing valid C pointer)


def test_exception_hierarchy():
    """Test exception inheritance hierarchy"""
    assert issubclass(ufbx.UfbxFileNotFoundError, ufbx.UfbxError)
    assert issubclass(ufbx.UfbxOutOfMemoryError, ufbx.UfbxError)
    assert issubclass(ufbx.UfbxIOError, ufbx.UfbxError)
    assert issubclass(ufbx.UfbxError, Exception)


def test_load_memory_empty():
    """Test loading empty data"""
    # Empty data should fail
    with pytest.raises(ufbx.UfbxError):
        ufbx.load_memory(b'')


def test_load_memory_invalid():
    """Test loading invalid data"""
    # Invalid FBX data should fail
    with pytest.raises(ufbx.UfbxError):
        ufbx.load_memory(b'not a valid fbx file')
