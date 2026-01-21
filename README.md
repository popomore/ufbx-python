# ufbx-python

[![PyPI version](https://badge.fury.io/py/pyufbx.svg)](https://badge.fury.io/py/pyufbx)
[![Tests](https://github.com/popomore/ufbx-python/workflows/Tests/badge.svg)](https://github.com/popomore/ufbx-python/actions/workflows/test.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/pyufbx.svg)](https://pypi.org/project/pyufbx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python bindings for [ufbx](https://github.com/ufbx/ufbx) - a single source file FBX loader library.

## Status

✅ **Feature Complete** - Full ufbx API coverage with comprehensive Python bindings

All major ufbx features are now accessible from Python:
- Complete scene loading and querying
- All element types with Pythonic wrappers
- Animation evaluation and manipulation
- Mesh operations and geometry processing
- Full math library (vectors, quaternions, matrices, transforms)

## Installation

```bash
pip install pyufbx
```

**Note**: The PyPI package name is `pyufbx`, but you import it as `ufbx`:

```python
import ufbx  # Not "import pyufbx"
```

Install from source:

```bash
git clone https://github.com/popomore/ufbx-python.git
cd ufbx-python
pip install .
```

## Technical Stack

- **Binding Method**: cffi (API mode)
- **Code Generation**: using automatic code generator
- **Dependency Management**: Using sfs.py to manage dependencies with exact commit hashes

## Quick Start

### Build from Source

```bash
# Install dependencies
python3 sfs.py update --all

# Build
./build.sh

# Or manual steps:
python3 bindgen/ufbx_parser.py -i ufbx-c/ufbx.h -o bindgen/build/ufbx.json
python3 bindgen/ufbx_ir.py
python3 bindgen/generate_python.py
python3 setup.py build_ext --inplace
```

### Usage Example

```python
import ufbx

# Load FBX file
with ufbx.load_file("model.fbx") as scene:
    # Basic scene info
    print(f"Nodes: {scene.node_count}")
    print(f"Meshes: {scene.mesh_count}")
    print(f"Materials: {scene.material_count}")
    print(f"Animations: {scene.animation_count}")

    # Access scene hierarchy
    for node in scene.nodes:
        print(f"Node: {node.name}")
        if node.mesh:
            mesh = node.mesh
            print(f"  Mesh: {mesh.num_vertices} vertices, {mesh.num_faces} faces")
        if node.light:
            print(f"  Light: {node.light.light_type}")
        if node.camera:
            print(f"  Camera: {node.camera.projection_mode}")

    # Access mesh data
    for mesh in scene.meshes:
        positions = mesh.vertex_position
        normals = mesh.vertex_normal
        uvs = mesh.vertex_uv
        print(f"Mesh '{mesh.name}': {len(positions)} vertices")

    # Math operations
    node = scene.find_node("MyNode")
    if node:
        transform = node.local_transform
        print(f"Translation: {transform.translation}")
        print(f"Rotation: {transform.rotation}")
        print(f"Scale: {transform.scale}")

        # Convert to matrix
        matrix = transform.to_matrix()
        print(f"Matrix: {matrix}")

# Or use class method
scene = ufbx.Scene.load_file("model.fbx")
try:
    # Use scene
    print(scene)
finally:
    scene.close()
```

Run example script:

```bash
python3 examples/basic_usage.py tests/data/your_model.fbx
```

## Current Progress

- [x] Project structure setup
- [x] Dependency management with sfs.py
- [x] Download ufbx source (commit: `6ecd6177af59c82ec363356ac36c3a4245b85321`)
- [x] Python code generator
- [x] Build system (setup.py, pyproject.toml, build.sh)
- [x] Generate cffi bindings (enums, structs, key functions)
- [x] Implement core API (Scene class, error handling)
- [x] **100% ufbx API coverage** - All element types, enums, and functions
- [x] Comprehensive test suite (27 tests all passing)
- [x] Write example code
- [x] Full element wrappers (Node, Mesh, Material, Light, Camera, Animation, Deformers, etc.)
- [x] Math types (Vec2, Vec3, Vec4, Quat, Matrix, Transform)
- [x] All 60+ enum types
- [ ] Add type hints (.pyi files)

## Dependency Management

This project uses [sfs.py](https://github.com/bqqbarbhg/sfs) for dependency management:

```bash
# Update dependencies
python3 sfs.py update --all

# View current version
cat sfs-deps.json.lock
```

## Features

- ✅ **Zero Dependencies**: Only requires cffi, no other runtime dependencies
- ✅ **Type Safe**: Complete error handling and exception hierarchy
- ✅ **Memory Management**: Automatic resource cleanup (RAII pattern)
- ✅ **Pythonic API**: Context managers, property access, Python idioms
- ✅ **100% API Coverage**: Complete bindings for all ufbx features
  - 38 Element types (Node, Mesh, Light, Camera, Material, Animation, Deformers, etc.)
  - 60+ Enum types (all ufbx enums fully exposed)
  - Math types (Vec2, Vec3, Vec4, Quat, Matrix, Transform)
  - Animation evaluation and baking
  - Mesh operations (triangulation, subdivision, topology)
  - Transform and hierarchy manipulation
  - Material and texture queries
  - Deformers (Skin, Blend, Cache)
  - Constraints and collections

## Development

### Build from Source

```bash
# Clone repository
git clone https://github.com/popomore/ufbx-python.git
cd ufbx-python

# Download dependencies
python3 sfs.py update --all

# Build
./build.sh

# Run tests
pytest tests/ -v
```

### Publishing to PyPI

See [Release Guide](RELEASING.md) for how to publish new versions to PyPI.

## References

- ufbx Documentation: https://ufbx.github.io/
- ufbx-rust Implementation: https://github.com/ufbx/ufbx-rust
- cffi Documentation: https://cffi.readthedocs.io/
- PyPI Project Page: https://pypi.org/project/pyufbx/

## License

MIT - See [LICENSE](LICENSE) file for details.

This project includes [ufbx](https://github.com/ufbx/ufbx), also under the MIT License.
