"""
Comprehensive tests for ufbx Python bindings
Tests all major API features and classes
"""

import ufbx


def test_all_enums_importable():
    """Test that all enum types can be imported and have values"""
    enums_to_test = [
        # Core enums
        'RotationOrder', 'ElementType', 'PropType', 'PropFlags',
        # Transform
        'InheritMode', 'MirrorAxis', 'CoordinateAxis',
        # Geometry
        'SubdivisionDisplayMode', 'SubdivisionBoundary',
        # Lights
        'LightType', 'LightDecay', 'LightAreaShape',
        # Cameras
        'ProjectionMode', 'AspectMode', 'ApertureMode',
        # Materials
        'ShaderType', 'TextureType', 'BlendMode', 'WrapMode',
        # Animation
        'Interpolation', 'ExtrapolationMode',
        # Constraints
        'ConstraintType',
        # Errors
        'ErrorType',
    ]

    for enum_name in enums_to_test:
        assert hasattr(ufbx, enum_name), f"Missing enum: {enum_name}"
        enum_class = getattr(ufbx, enum_name)
        # Check that enum has at least one value
        assert len(list(enum_class)) > 0, f"Enum {enum_name} has no values"


def test_all_element_classes_importable():
    """Test that all element wrapper classes can be imported"""
    classes_to_test = [
        'Scene', 'Element', 'Node', 'Mesh',
        'Light', 'Camera', 'Bone',
        'Material', 'Texture',
        'Anim', 'AnimStack', 'AnimLayer', 'AnimCurve',
        'SkinDeformer', 'SkinCluster',
        'BlendDeformer', 'BlendChannel', 'BlendShape',
        'Constraint',
    ]

    for class_name in classes_to_test:
        assert hasattr(ufbx, class_name), f"Missing class: {class_name}"
        cls = getattr(ufbx, class_name)
        assert callable(cls), f"{class_name} is not a class"


def test_math_types():
    """Test math type wrappers"""
    # Test Vec2
    v2 = ufbx.Vec2(1.0, 2.0)
    assert v2.x == 1.0
    assert v2.y == 2.0
    assert list(v2) == [1.0, 2.0]
    assert "Vec2" in repr(v2)

    # Test Vec3
    v3 = ufbx.Vec3(1.0, 2.0, 3.0)
    assert v3.x == 1.0
    assert v3.y == 2.0
    assert v3.z == 3.0
    assert list(v3) == [1.0, 2.0, 3.0]
    assert "Vec3" in repr(v3)

    # Test Vec4
    v4 = ufbx.Vec4(1.0, 2.0, 3.0, 4.0)
    assert v4.x == 1.0
    assert v4.y == 2.0
    assert v4.z == 3.0
    assert v4.w == 4.0
    assert list(v4) == [1.0, 2.0, 3.0, 4.0]

    # Test Quat
    q = ufbx.Quat(0.0, 0.0, 0.0, 1.0)
    assert q.x == 0.0
    assert q.y == 0.0
    assert q.z == 0.0
    assert q.w == 1.0
    assert "Quat" in repr(q)

    # Test Matrix
    m = ufbx.Matrix()
    assert m.m is not None
    assert len(m.m) == 3
    assert len(m.m[0]) == 4

    # Test Transform
    t = ufbx.Transform()
    assert t.translation is not None
    assert t.rotation is not None
    assert t.scale is not None
    assert isinstance(t.translation, ufbx.Vec3)
    assert isinstance(t.rotation, ufbx.Quat)
    assert isinstance(t.scale, ufbx.Vec3)


def test_vec3_normalize():
    """Test Vec3 normalize method"""
    v = ufbx.Vec3(3.0, 4.0, 0.0)
    normalized = v.normalize()
    # Length should be approximately 1.0
    length = (normalized.x**2 + normalized.y**2 + normalized.z**2)**0.5
    assert abs(length - 1.0) < 0.0001


def test_quat_operations():
    """Test quaternion operations"""
    q1 = ufbx.Quat(0.0, 0.0, 0.0, 1.0)
    q2 = ufbx.Quat(0.0, 0.0, 0.0, 1.0)

    # Test multiplication
    q3 = q1 * q2
    assert isinstance(q3, ufbx.Quat)

    # Test normalize
    q_normalized = q1.normalize()
    assert isinstance(q_normalized, ufbx.Quat)


def test_convenience_functions():
    """Test convenience functions"""
    assert callable(ufbx.load_file)
    assert callable(ufbx.load_memory)


def test_error_hierarchy():
    """Test exception hierarchy"""
    assert issubclass(ufbx.UfbxFileNotFoundError, ufbx.UfbxError)
    assert issubclass(ufbx.UfbxOutOfMemoryError, ufbx.UfbxError)
    assert issubclass(ufbx.UfbxIOError, ufbx.UfbxError)
    assert issubclass(ufbx.UfbxError, Exception)


def test_file_not_found():
    """Test that loading non-existent file raises proper exception"""
    try:
        ufbx.load_file('nonexistent_file_12345.fbx')
        assert False, "Should have raised UfbxFileNotFoundError"
    except ufbx.UfbxFileNotFoundError as e:
        assert 'nonexistent_file_12345.fbx' in str(e)


def test_load_invalid_memory():
    """Test loading invalid data from memory"""
    try:
        ufbx.load_memory(b'not a valid fbx file')
        assert False, "Should have raised UfbxError"
    except ufbx.UfbxError:
        pass  # Expected


def test_rotation_order_enum():
    """Test RotationOrder enum"""
    assert hasattr(ufbx.RotationOrder, 'ROTATION_ORDER_XYZ')
    assert hasattr(ufbx.RotationOrder, 'ROTATION_ORDER_XZY')
    assert hasattr(ufbx.RotationOrder, 'ROTATION_ORDER_YZX')

    assert isinstance(ufbx.RotationOrder.ROTATION_ORDER_XYZ.value, int)


def test_element_type_enum():
    """Test ElementType enum"""
    assert hasattr(ufbx.ElementType, 'ELEMENT_NODE')
    assert hasattr(ufbx.ElementType, 'ELEMENT_MESH')
    assert hasattr(ufbx.ElementType, 'ELEMENT_LIGHT')
    assert hasattr(ufbx.ElementType, 'ELEMENT_CAMERA')
    assert hasattr(ufbx.ElementType, 'ELEMENT_MATERIAL')


def test_light_type_enum():
    """Test LightType enum"""
    assert hasattr(ufbx.LightType, 'LIGHT_POINT')
    assert hasattr(ufbx.LightType, 'LIGHT_DIRECTIONAL')
    assert hasattr(ufbx.LightType, 'LIGHT_SPOT')


def test_camera_projection_enum():
    """Test ProjectionMode enum"""
    assert hasattr(ufbx.ProjectionMode, 'PROJECTION_MODE_PERSPECTIVE')
    assert hasattr(ufbx.ProjectionMode, 'PROJECTION_MODE_ORTHOGRAPHIC')


def test_shader_type_enum():
    """Test ShaderType enum"""
    assert hasattr(ufbx.ShaderType, 'SHADER_FBX_LAMBERT')
    assert hasattr(ufbx.ShaderType, 'SHADER_FBX_PHONG')


def test_interpolation_enum():
    """Test Interpolation enum"""
    assert hasattr(ufbx.Interpolation, 'INTERPOLATION_CONSTANT_PREV')
    assert hasattr(ufbx.Interpolation, 'INTERPOLATION_CONSTANT_NEXT')
    assert hasattr(ufbx.Interpolation, 'INTERPOLATION_LINEAR')
    assert hasattr(ufbx.Interpolation, 'INTERPOLATION_CUBIC')


def test_constraint_type_enum():
    """Test ConstraintType enum"""
    assert hasattr(ufbx.ConstraintType, 'CONSTRAINT_AIM')
    assert hasattr(ufbx.ConstraintType, 'CONSTRAINT_PARENT')


def test_error_type_enum():
    """Test ErrorType enum"""
    assert hasattr(ufbx.ErrorType, 'ERROR_NONE')
    assert hasattr(ufbx.ErrorType, 'ERROR_FILE_NOT_FOUND')
    assert hasattr(ufbx.ErrorType, 'ERROR_OUT_OF_MEMORY')


def test_api_coverage_stats():
    """Print API coverage statistics"""
    exported_count = len(ufbx.__all__)
    classes = [x for x in ufbx.__all__ if x[0].isupper() and x not in ['Vec2', 'Vec3', 'Vec4', 'Quat', 'Matrix', 'Transform']]

    print("\n=== ufbx Python Bindings Coverage ===")
    print(f"Total exported symbols: {exported_count}")
    print(f"Element/Enum classes: {len(classes)}")
    print("Math types: 6 (Vec2, Vec3, Vec4, Quat, Matrix, Transform)")
    print("Core functions: load_file, load_memory")
    print("Exception types: 4 (UfbxError, UfbxFileNotFoundError, UfbxIOError, UfbxOutOfMemoryError)")


def test_version():
    """Test version is defined"""
    assert hasattr(ufbx, '__version__')
    assert isinstance(ufbx.__version__, str)


if __name__ == '__main__':
    # Run all tests
    import sys

    test_functions = [
        test_all_enums_importable,
        test_all_element_classes_importable,
        test_math_types,
        test_vec3_normalize,
        test_quat_operations,
        test_convenience_functions,
        test_error_hierarchy,
        test_file_not_found,
        test_load_invalid_memory,
        test_rotation_order_enum,
        test_element_type_enum,
        test_light_type_enum,
        test_camera_projection_enum,
        test_shader_type_enum,
        test_interpolation_enum,
        test_constraint_type_enum,
        test_error_type_enum,
        test_api_coverage_stats,
        test_version,
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
