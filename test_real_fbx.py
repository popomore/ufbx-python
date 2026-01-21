#!/usr/bin/env python3
"""
Test script to verify ufbx Python bindings with a real FBX file
"""

import os
import sys

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import ufbx


def test_load_fbx():
    """Load and inspect a real FBX file"""
    fbx_file = "tests/data/maya_cube.fbx"

    if not os.path.exists(fbx_file):
        print(f"Error: {fbx_file} not found")
        return False

    print(f"Loading FBX file: {fbx_file}")
    print("=" * 60)

    try:
        with ufbx.load_file(fbx_file) as scene:
            print("\n✓ Successfully loaded scene!")
            print("\nScene Statistics:")
            print(f"  Nodes:      {scene.node_count}")
            print(f"  Meshes:     {scene.mesh_count}")
            print(f"  Materials:  {scene.material_count}")
            print(f"  Textures:   {scene.texture_count}")
            print(f"  Lights:     {scene.light_count}")
            print(f"  Cameras:    {scene.camera_count}")
            print(f"  Animations: {scene.animation_count}")

            # Inspect nodes
            print(f"\n{'-' * 60}")
            print("Node Hierarchy:")
            print(f"{'-' * 60}")
            for i, node in enumerate(scene.nodes):
                indent = "  " * (0 if node.is_root else 1)
                print(f"{indent}[{i}] {node.name} (id={node.element_id})")

                if node.mesh:
                    mesh = node.mesh
                    print(f"{indent}    Mesh: {mesh.num_vertices} verts, {mesh.num_faces} faces")

                if node.light:
                    print(f"{indent}    Light type: {node.light.light_type}")

                if node.camera:
                    print(f"{indent}    Camera projection: {node.camera.projection_mode}")

                # Show transform
                t = node.local_transform
                print(f"{indent}    Position: ({t.translation.x:.2f}, {t.translation.y:.2f}, {t.translation.z:.2f})")
                print(f"{indent}    Scale: ({t.scale.x:.2f}, {t.scale.y:.2f}, {t.scale.z:.2f})")

            # Inspect meshes
            if scene.mesh_count > 0:
                print(f"\n{'-' * 60}")
                print("Mesh Details:")
                print(f"{'-' * 60}")
                for i, mesh in enumerate(scene.meshes):
                    print(f"\n[{i}] Mesh '{mesh.name}':")
                    print(f"  Vertices: {mesh.num_vertices}")
                    print(f"  Indices:  {mesh.num_indices}")
                    print(f"  Faces:    {mesh.num_faces}")
                    print(f"  Triangles: {mesh.num_triangles}")

                    # Show first few vertices
                    positions = mesh.vertex_position
                    if len(positions) > 0:
                        print("  First 3 vertices:")
                        for j in range(min(3, len(positions))):
                            v = positions[j]
                            print(f"    [{j}] ({v.x:.3f}, {v.y:.3f}, {v.z:.3f})")

                    # Test triangulation
                    if mesh.num_faces > 0:
                        try:
                            triangles = mesh.triangulate_face(0)
                            print(f"  Face 0 triangulation: {len(triangles) // 3} triangles")
                        except Exception as e:
                            print(f"  Triangulation error: {e}")

            # Inspect materials
            if scene.material_count > 0:
                print(f"\n{'-' * 60}")
                print("Materials:")
                print(f"{'-' * 60}")
                for i, material in enumerate(scene.materials):
                    print(f"[{i}] Material '{material.name}' (shader type: {material.shader_type})")
                    if len(material.textures) > 0:
                        print(f"    Textures: {len(material.textures)}")

            # Test math operations
            print(f"\n{'-' * 60}")
            print("Math Operations Test:")
            print(f"{'-' * 60}")

            v1 = ufbx.Vec3(1.0, 0.0, 0.0)
            v2 = v1.normalize()
            print(f"Vec3 normalize: {v1} -> {v2}")

            q1 = ufbx.Quat(0.0, 0.0, 0.0, 1.0)
            q2 = q1.normalize()
            print(f"Quat normalize: {q1} -> {q2}")

            q3 = q1 * q2
            print(f"Quat multiply: {q1} * {q2} = {q3}")

            # Test transform to matrix conversion
            if scene.node_count > 0:
                node = scene.nodes[0]
                transform = node.local_transform
                matrix = transform.to_matrix()
                print(f"Transform to matrix: {len(matrix.m)} rows")

            print(f"\n{'=' * 60}")
            print("✓ All tests passed!")
            print(f"{'=' * 60}")

            return True

    except ufbx.UfbxError as e:
        print(f"\n✗ Error loading FBX: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_load_fbx()
    sys.exit(0 if success else 1)
