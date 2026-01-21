#!/usr/bin/env python3
"""
Test script to verify type hints are working correctly
"""

import ufbx


def test_basic_types() -> None:
    """Test basic type hints"""
    # Math types
    v2: ufbx.Vec2 = ufbx.Vec2(1.0, 2.0)
    v3: ufbx.Vec3 = ufbx.Vec3(1.0, 2.0, 3.0)
    v4: ufbx.Vec4 = ufbx.Vec4(1.0, 2.0, 3.0, 4.0)
    q: ufbx.Quat = ufbx.Quat(0.0, 0.0, 0.0, 1.0)
    m: ufbx.Matrix = ufbx.Matrix()
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
        scene: ufbx.Scene = ufbx.load_file("nonexistent.fbx")
    except ufbx.UfbxFileNotFoundError as e:
        error: ufbx.UfbxFileNotFoundError = e
        assert isinstance(error, ufbx.UfbxError)


def test_scene_properties() -> None:
    """Test scene properties type hints"""
    # Mock scene (will fail at runtime but type hints should work)
    try:
        scene = ufbx.load_file("test.fbx")

        # Test property types
        nodes: list[ufbx.Node] = scene.nodes
        meshes: list[ufbx.Mesh] = scene.meshes
        materials: list[ufbx.Material] = scene.materials
        lights: list[ufbx.Light] = scene.lights
        cameras: list[ufbx.Camera] = scene.cameras

        # Test counts
        node_count: int = scene.node_count
        mesh_count: int = scene.mesh_count

        # Test find methods
        node: ufbx.Node | None = scene.find_node("MyNode")
        material: ufbx.Material | None = scene.find_material("MyMaterial")

        scene.close()
    except ufbx.UfbxError:
        pass


def test_node_properties() -> None:
    """Test node properties type hints"""
    try:
        scene = ufbx.load_file("test.fbx")
        if scene.node_count > 0:
            node: ufbx.Node = scene.nodes[0]

            # Test properties
            name: str = node.name
            elem_id: int = node.element_id
            visible: bool = node.visible
            is_root: bool = node.is_root

            # Test optional properties
            parent: ufbx.Node | None = node.parent
            mesh: ufbx.Mesh | None = node.mesh
            light: ufbx.Light | None = node.light
            camera: ufbx.Camera | None = node.camera

            # Test transforms
            transform: ufbx.Transform = node.local_transform
            matrix: ufbx.Matrix = node.node_to_world

            # Test lists
            children: list[ufbx.Node] = node.children
            materials: list[ufbx.Material] = node.materials

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
            num_verts: int = mesh.num_vertices
            num_faces: int = mesh.num_faces
            num_indices: int = mesh.num_indices

            # Test vertex data
            positions: list[ufbx.Vec3] = mesh.vertex_position
            normals: list[ufbx.Vec3] = mesh.vertex_normal
            uvs: list[ufbx.Vec2] = mesh.vertex_uv

            # Test deformers
            skin_deformers: list[ufbx.SkinDeformer] = mesh.skin_deformers
            blend_deformers: list[ufbx.BlendDeformer] = mesh.blend_deformers

            # Test methods
            indices: list[int] = mesh.triangulate_face(0)

        scene.close()
    except ufbx.UfbxError:
        pass


def test_enums() -> None:
    """Test enum type hints"""
    # Test enum access
    rot_order: ufbx.RotationOrder = ufbx.RotationOrder.ROTATION_ORDER_XYZ
    light_type: ufbx.LightType = ufbx.LightType.LIGHT_POINT
    proj_mode: ufbx.ProjectionMode = ufbx.ProjectionMode.PROJECTION_MODE_PERSPECTIVE

    # Test enum values
    assert isinstance(rot_order.value, int)
    assert isinstance(light_type.value, int)


if __name__ == "__main__":
    print("Testing type hints...")
    print("✓ All type annotations are syntactically correct")
    print("Run 'mypy test_type_hints.py' to verify type checking")
