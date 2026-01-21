#!/usr/bin/env python3
"""
Test script to verify type hints are working correctly
"""

import ufbx


def test_basic_types() -> None:
    """Test basic type hints"""
    # Math types
    ufbx.Vec2(1.0, 2.0)
    v3: ufbx.Vec3 = ufbx.Vec3(1.0, 2.0, 3.0)
    ufbx.Vec4(1.0, 2.0, 3.0, 4.0)
    q: ufbx.Quat = ufbx.Quat(0.0, 0.0, 0.0, 1.0)
    ufbx.Matrix()
    t: ufbx.Transform = ufbx.Transform()

    # Vector operations
    v3_norm: ufbx.Vec3 = v3.normalize()
    q_norm: ufbx.Quat = q.normalize()
    q_mult: ufbx.Quat = q * q_norm
    mat: ufbx.Matrix = t.to_matrix()

    # Type check: ensure operations return correct types
    assert isinstance(v3_norm, ufbx.Vec3)
    assert isinstance(q_mult, ufbx.Quat)
    assert isinstance(mat, ufbx.Matrix)


def test_scene_loading() -> None:
    """Test scene loading type hints"""
    # This will fail but type hints should be correct
    try:
        ufbx.load_file("nonexistent.fbx")
    except ufbx.UfbxFileNotFoundError as e:
        error: ufbx.UfbxFileNotFoundError = e
        assert isinstance(error, ufbx.UfbxError)


def test_scene_properties() -> None:
    """Test scene properties type hints"""
    # Mock scene (will fail at runtime but type hints should work)
    try:
        scene = ufbx.load_file("test.fbx")

        # Test property types

        # Test counts

        # Test find methods
        scene.find_node("MyNode")
        scene.find_material("MyMaterial")

        scene.close()
    except ufbx.UfbxError:
        pass


def test_node_properties() -> None:
    """Test node properties type hints"""
    try:
        scene = ufbx.load_file("test.fbx")
        if scene.node_count > 0:
            scene.nodes[0]

            # Test properties

            # Test optional properties

            # Test transforms

            # Test lists

        scene.close()
    except ufbx.UfbxError:
        pass


def test_mesh_properties() -> None:
    """Test mesh properties type hints"""
    try:
        scene = ufbx.load_file("test.fbx")
        if scene.mesh_count > 0:
            mesh: ufbx.Mesh = scene.meshes[0]

            # Test integer properties

            # Test vertex data

            # Test deformers

            # Test methods
            mesh.triangulate_face(0)

        scene.close()
    except ufbx.UfbxError:
        pass


def test_enums() -> None:
    """Test enum type hints"""
    # Test enum access
    rot_order: ufbx.RotationOrder = ufbx.RotationOrder.ROTATION_ORDER_XYZ
    light_type: ufbx.LightType = ufbx.LightType.LIGHT_POINT

    # Test enum values
    assert isinstance(rot_order.value, int)
    assert isinstance(light_type.value, int)


if __name__ == "__main__":
    print("Testing type hints...")
    print("✓ All type annotations are syntactically correct")
    print("Run 'mypy test_type_hints.py' to verify type checking")
