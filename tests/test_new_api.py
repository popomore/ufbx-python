"""
Test new API functionality for Light, Camera, Bone, and Texture
"""

import ufbx


def test_scene_has_new_properties():
    """Test that Scene has the new properties"""
    # We can't test with real FBX data without files, but we can verify
    # the properties exist and are callable
    assert hasattr(ufbx.Scene, 'lights')
    assert hasattr(ufbx.Scene, 'cameras')
    assert hasattr(ufbx.Scene, 'bones')
    assert hasattr(ufbx.Scene, 'textures')


def test_node_has_new_properties():
    """Test that Node has the new properties"""
    assert hasattr(ufbx.Node, 'light')
    assert hasattr(ufbx.Node, 'camera')
    assert hasattr(ufbx.Node, 'bone')


def test_light_class_has_properties():
    """Test that Light class has expected properties"""
    expected_properties = [
        'name', 'color', 'intensity', 'local_direction',
        'type', 'decay', 'area_shape', 'inner_angle',
        'outer_angle', 'cast_light', 'cast_shadows'
    ]
    for prop in expected_properties:
        assert hasattr(ufbx.Light, prop), f"Light missing property: {prop}"


def test_camera_class_has_properties():
    """Test that Camera class has expected properties"""
    expected_properties = [
        'name', 'projection_mode', 'resolution', 'resolution_is_pixels',
        'field_of_view_deg', 'field_of_view_tan', 'orthographic_extent',
        'orthographic_size', 'aspect_ratio', 'near_plane', 'far_plane'
    ]
    for prop in expected_properties:
        assert hasattr(ufbx.Camera, prop), f"Camera missing property: {prop}"


def test_bone_class_has_properties():
    """Test that Bone class has expected properties"""
    expected_properties = ['name', 'radius', 'relative_length', 'is_root']
    for prop in expected_properties:
        assert hasattr(ufbx.Bone, prop), f"Bone missing property: {prop}"


def test_texture_class_has_properties():
    """Test that Texture class has expected properties"""
    expected_properties = [
        'name', 'filename', 'absolute_filename',
        'relative_filename', 'type'
    ]
    for prop in expected_properties:
        assert hasattr(ufbx.Texture, prop), f"Texture missing property: {prop}"


def test_light_camera_bone_are_elements():
    """Test that Light, Camera, and Bone are subclasses of Element"""
    assert issubclass(ufbx.Light, ufbx.Element)
    assert issubclass(ufbx.Camera, ufbx.Element)
    assert issubclass(ufbx.Bone, ufbx.Element)
    assert issubclass(ufbx.Texture, ufbx.Element)


if __name__ == "__main__":
    import sys

    test_functions = [
        test_scene_has_new_properties,
        test_node_has_new_properties,
        test_light_class_has_properties,
        test_camera_class_has_properties,
        test_bone_class_has_properties,
        test_texture_class_has_properties,
        test_light_camera_bone_are_elements,
    ]

    failed = 0
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
        except Exception as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1

    print(f"\n{len(test_functions) - failed}/{len(test_functions)} tests passed")
    sys.exit(0 if failed == 0 else 1)
