# ufbx-python

[![PyPI version](https://badge.fury.io/py/ufbx.svg)](https://badge.fury.io/py/ufbx)
[![Tests](https://github.com/popomore/ufbx-python/workflows/Tests/badge.svg)](https://github.com/popomore/ufbx-python/actions/workflows/test.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/ufbx.svg)](https://pypi.org/project/ufbx/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python bindings for [ufbx](https://github.com/ufbx/ufbx) - a single source file FBX loader library.

## Status

🚧 **Under Development** - This project is actively being developed

## Installation

```bash
pip install ufbx
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
    print(f"Nodes: {scene.node_count}")
    print(f"Meshes: {scene.mesh_count}")
    print(f"Materials: {scene.material_count}")
    print(f"Animations: {scene.animation_count}")

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
- [x] Write basic test suite (8 tests all passing)
- [x] Write example code
- [ ] Extend API (Node, Mesh, Material class wrappers)
- [ ] Add more test cases
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
- PyPI Project Page: https://pypi.org/project/ufbx/

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) (to be created) for details.

## License

MIT - See [LICENSE](LICENSE) file for details.

This project includes [ufbx](https://github.com/ufbx/ufbx), also under the MIT License.
