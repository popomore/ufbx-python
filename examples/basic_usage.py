#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates how to use ufbx-python to load FBX files
"""

import ufbx
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 basic_usage.py <fbx_file_path>")
        print("\nExample:")
        print("  python3 basic_usage.py model.fbx")
        sys.exit(1)

    filename = sys.argv[1]

    print(f"=== ufbx-python Basic Usage Example ===")
    print(f"Version: {ufbx.__version__}")
    print()

    try:
        # Load scene using context manager
        with ufbx.load_file(filename) as scene:
            print(f"Successfully loaded: {filename}")
            print()
            print(f"Scene statistics:")
            print(f"  - Node count: {scene.node_count}")
            print(f"  - Mesh count: {scene.mesh_count}")
            print(f"  - Material count: {scene.material_count}")
            print(f"  - Animation count: {scene.animation_count}")
            print()
            print(f"Scene object: {scene}")

    except ufbx.UfbxFileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except ufbx.UfbxError as e:
        print(f"Error: Load failed - {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
