#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates how to use ufbx-python to load FBX files
"""

import sys

import ufbx


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 basic_usage.py <fbx_file_path>")
        print("\nExample:")
        print("  python3 basic_usage.py model.fbx")
        sys.exit(1)

    filename = sys.argv[1]

    print("=== ufbx-python Basic Usage Example ===")
    print(f"Version: {ufbx.__version__}")
    print()

    try:
        # Load scene using context manager
        with ufbx.load_file(filename) as scene:
            print(f"Successfully loaded: {filename}")
            print()

            # Scene statistics
            print("Scene statistics:")
            print(f"  - Nodes: {len(scene.nodes)}")
            print(f"  - Meshes: {len(scene.meshes)}")
            print(f"  - Materials: {len(scene.materials)}")
            print()

            # Root node info
            root = scene.root_node
            if root:
                print(f"Root node: '{root.name}' (children: {len(root.children)})")
                print()

            # List first few nodes
            print("First 5 nodes:")
            for i, node in enumerate(scene.nodes[:5]):
                mesh_info = " [has mesh]" if node.mesh else ""
                print(f"  {i}: {node.name}{mesh_info}")
            print()

            # List meshes with vertex counts
            if scene.meshes:
                print("Meshes:")
                for i, mesh in enumerate(scene.meshes):
                    print(f"  {i}: {mesh.name} ({mesh.num_vertices} vertices)")
                print()

            # Show first mesh details
            if scene.meshes:
                mesh = scene.meshes[0]
                print(f"First mesh details: {mesh.name}")
                print(f"  Vertices: {mesh.num_vertices}")
                print(f"  Indices: {mesh.num_indices}")
                print(f"  Faces: {mesh.num_faces}")
                print(f"  Triangles: {mesh.num_triangles}")

                # Access vertex data (numpy arrays)
                positions = mesh.vertex_positions
                if positions is not None:
                    print(f"  Vertex positions: shape={positions.shape}, dtype={positions.dtype}")
                    if len(positions) > 0:
                        print(f"    First vertex: {positions[0]}")

                print()

    except FileNotFoundError:
        print(f"Error: File not found - {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Load failed - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
