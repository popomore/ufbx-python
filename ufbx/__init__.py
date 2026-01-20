"""
ufbx - Python bindings for ufbx FBX loader

High-performance Python bindings for the ufbx FBX file loader library.

Basic usage:
    >>> import ufbx
    >>> with ufbx.load_file("model.fbx") as scene:
    ...     print(f"Loaded {scene.node_count} nodes")

https://github.com/ufbx/ufbx
"""

__version__ = '0.1.0'

# Export core API
from ufbx.core import Scene, load_file, load_memory
from ufbx.errors import (
    UfbxError,
    UfbxFileNotFoundError,
    UfbxIOError,
    UfbxOutOfMemoryError,
)

# Export generated enums (example)
from ufbx.generated import RotationOrder

__all__ = [
    # Version
    "__version__",
    # Core classes
    "Scene",
    # Convenience functions
    "load_file",
    "load_memory",
    # Exceptions
    "UfbxError",
    "UfbxFileNotFoundError",
    "UfbxOutOfMemoryError",
    "UfbxIOError",
    # Enums
    "RotationOrder",
]
