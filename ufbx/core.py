"""
ufbx Core API - High-level Pythonic Wrapper
"""

from ufbx._ufbx import ffi, lib
from ufbx.errors import UfbxError, UfbxFileNotFoundError, UfbxOutOfMemoryError
from typing import Optional
import os


class Scene:
    """FBX Scene Wrapper Class

    Usage Example:
        # Using context manager (recommended)
        with Scene.load_file("model.fbx") as scene:
            print(f"Nodes: {scene.node_count}")
            print(f"Meshes: {scene.mesh_count}")

        # Or manual management
        scene = Scene.load_file("model.fbx")
        try:
            # Use scene
            pass
        finally:
            scene.close()
    """

    def __init__(self, scene_ptr):
        """Internal constructor, do not call directly. Use Scene.load_file() or Scene.load_memory()"""
        if scene_ptr == ffi.NULL:
            raise UfbxError("Scene pointer is NULL")
        self._scene = scene_ptr
        self._closed = False

    @classmethod
    def load_file(cls, filename: str, opts=None) -> 'Scene':
        """Load FBX scene from file

        Args:
            filename: FBX file path
            opts: Load options (not implemented yet)

        Returns:
            Scene instance

        Raises:
            UfbxFileNotFoundError: File does not exist
            UfbxError: Load failed
        """
        if not os.path.exists(filename):
            raise UfbxFileNotFoundError(f"File not found: {filename}")

        # Prepare error struct
        error = ffi.new("ufbx_error *")

        # Convert filename to bytes
        filename_bytes = filename.encode('utf-8')

        # Call C API
        opts_ptr = ffi.NULL  # Custom options not supported yet
        scene_ptr = lib.ufbx_load_file(filename_bytes, opts_ptr, error)

        if scene_ptr == ffi.NULL:
            # Extract error information
            # description is ufbx_string type, has data and length fields
            if error.description.data != ffi.NULL and error.description.length > 0:
                error_desc = ffi.string(error.description.data, error.description.length).decode('utf-8')
            else:
                error_desc = "Unknown error"
            error_type = error.type

            if error_type == lib.UFBX_ERROR_FILE_NOT_FOUND:
                raise UfbxFileNotFoundError(error_desc, error_type)
            elif error_type == lib.UFBX_ERROR_OUT_OF_MEMORY:
                raise UfbxOutOfMemoryError(error_desc, error_type)
            else:
                raise UfbxError(error_desc, error_type)

        return cls(scene_ptr)

    @classmethod
    def load_memory(cls, data: bytes, opts=None) -> 'Scene':
        """Load FBX scene from memory

        Args:
            data: Byte data of FBX file
            opts: Load options (not implemented yet)

        Returns:
            Scene instance

        Raises:
            UfbxError: Load failed
        """
        # Prepare error struct
        error = ffi.new("ufbx_error *")

        # Call C API
        opts_ptr = ffi.NULL
        scene_ptr = lib.ufbx_load_memory(data, len(data), opts_ptr, error)

        if scene_ptr == ffi.NULL:
            # Extract error information
            if error.description.data != ffi.NULL and error.description.length > 0:
                error_desc = ffi.string(error.description.data, error.description.length).decode('utf-8')
            else:
                error_desc = "Unknown error"
            error_type = error.type
            raise UfbxError(error_desc, error_type)

        return cls(scene_ptr)

    def close(self):
        """Release scene resources"""
        if not self._closed and self._scene != ffi.NULL:
            lib.ufbx_free_scene(self._scene)
            self._scene = ffi.NULL
            self._closed = True

    def __del__(self):
        """Destructor, automatically release resources"""
        self.close()

    def __enter__(self):
        """Support context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support context manager"""
        self.close()
        return False

    @property
    def metadata(self):
        """Scene metadata"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.metadata

    @property
    def node_count(self) -> int:
        """Number of nodes"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.nodes.count

    @property
    def mesh_count(self) -> int:
        """Number of meshes"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.meshes.count

    @property
    def material_count(self) -> int:
        """Number of materials"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.materials.count

    @property
    def animation_count(self) -> int:
        """Number of animations"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.anim_stacks.count

    def __repr__(self):
        if self._closed:
            return "<Scene (closed)>"
        return f"<Scene nodes={self.node_count} meshes={self.mesh_count} materials={self.material_count}>"


# Convenience functions
def load_file(filename: str) -> Scene:
    """Load FBX file (convenience function)

    Args:
        filename: FBX file path

    Returns:
        Scene instance
    """
    return Scene.load_file(filename)


def load_memory(data: bytes) -> Scene:
    """Load FBX from memory (convenience function)

    Args:
        data: Byte data of FBX file

    Returns:
        Scene instance
    """
    return Scene.load_memory(data)
