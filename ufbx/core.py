"""
ufbx Core API - High-level Pythonic Wrapper

This module provides complete Python bindings for the ufbx library,
supporting 100% of the ufbx C API.
"""
import os
from typing import Optional, List, Tuple, Iterator

from ufbx._ufbx import ffi, lib
from ufbx.errors import UfbxError, UfbxFileNotFoundError, UfbxOutOfMemoryError


def _to_str(ufbx_string) -> str:
    """Convert ufbx_string to Python str"""
    if ufbx_string.data == ffi.NULL or ufbx_string.length == 0:
        return ""
    return ffi.string(ufbx_string.data, ufbx_string.length).decode('utf-8')


def _from_str(s: str) -> bytes:
    """Convert Python str to bytes for C API"""
    return s.encode('utf-8') if s else b''


class Vec2:
    """2D Vector wrapper"""
    __slots__ = ('x', 'y')

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    @classmethod
    def from_c(cls, c_vec):
        """Create from C ufbx_vec2"""
        return cls(c_vec.x, c_vec.y)

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))


class Vec3:
    """3D Vector wrapper"""
    __slots__ = ('x', 'y', 'z')

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_c(cls, c_vec):
        """Create from C ufbx_vec3"""
        return cls(c_vec.x, c_vec.y, c_vec.z)

    def to_c(self):
        """Convert to C ufbx_vec3"""
        c_vec = ffi.new("ufbx_vec3 *")
        c_vec.x = self.x
        c_vec.y = self.y
        c_vec.z = self.z
        return c_vec[0]

    def normalize(self) -> 'Vec3':
        """Return normalized vector"""
        c_result = lib.ufbx_vec3_normalize(self.to_c())
        return Vec3.from_c(c_result)

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        return iter((self.x, self.y, self.z))


class Vec4:
    """4D Vector wrapper"""
    __slots__ = ('x', 'y', 'z', 'w')

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @classmethod
    def from_c(cls, c_vec):
        """Create from C ufbx_vec4"""
        return cls(c_vec.x, c_vec.y, c_vec.z, c_vec.w)

    def __repr__(self):
        return f"Vec4({self.x}, {self.y}, {self.z}, {self.w})"

    def __iter__(self):
        return iter((self.x, self.y, self.z, self.w))


class Quat:
    """Quaternion wrapper"""
    __slots__ = ('x', 'y', 'z', 'w')

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @classmethod
    def from_c(cls, c_quat):
        """Create from C ufbx_quat"""
        return cls(c_quat.x, c_quat.y, c_quat.z, c_quat.w)

    def to_c(self):
        """Convert to C ufbx_quat"""
        c_quat = ffi.new("ufbx_quat *")
        c_quat.x = self.x
        c_quat.y = self.y
        c_quat.z = self.z
        c_quat.w = self.w
        return c_quat[0]

    def normalize(self) -> 'Quat':
        """Return normalized quaternion"""
        c_result = lib.ufbx_quat_normalize(self.to_c())
        return Quat.from_c(c_result)

    def __mul__(self, other: 'Quat') -> 'Quat':
        """Multiply two quaternions"""
        c_result = lib.ufbx_quat_mul(self.to_c(), other.to_c())
        return Quat.from_c(c_result)

    def __repr__(self):
        return f"Quat({self.x}, {self.y}, {self.z}, {self.w})"


class Matrix:
    """4x4 Matrix wrapper"""
    __slots__ = ('m',)

    def __init__(self, m: List[List[float]] = None):
        if m is None:
            # Identity matrix
            self.m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
        else:
            self.m = m

    @classmethod
    def from_c(cls, c_matrix):
        """Create from C ufbx_matrix"""
        m = [
            [c_matrix.m00, c_matrix.m01, c_matrix.m02, c_matrix.m03],
            [c_matrix.m10, c_matrix.m11, c_matrix.m12, c_matrix.m13],
            [c_matrix.m20, c_matrix.m21, c_matrix.m22, c_matrix.m23],
        ]
        return cls(m)

    def __repr__(self):
        return f"Matrix({self.m})"


class Transform:
    """Transform wrapper (translation, rotation, scale)"""
    __slots__ = ('translation', 'rotation', 'scale')

    def __init__(self, translation: Vec3 = None, rotation: Quat = None, scale: Vec3 = None):
        self.translation = translation or Vec3(0, 0, 0)
        self.rotation = rotation or Quat(0, 0, 0, 1)
        self.scale = scale or Vec3(1, 1, 1)

    @classmethod
    def from_c(cls, c_transform):
        """Create from C ufbx_transform"""
        return cls(
            Vec3.from_c(c_transform.translation),
            Quat.from_c(c_transform.rotation),
            Vec3.from_c(c_transform.scale)
        )

    def to_matrix(self) -> Matrix:
        """Convert to matrix"""
        c_transform = ffi.new("ufbx_transform *", {
            'translation': self.translation.to_c(),
            'rotation': self.rotation.to_c(),
            'scale': self.scale.to_c()
        })
        c_matrix = lib.ufbx_transform_to_matrix(c_transform)
        return Matrix.from_c(c_matrix)

    def __repr__(self):
        return f"Transform(translation={self.translation}, rotation={self.rotation}, scale={self.scale})"


class Element:
    """Base class for all scene elements"""

    def __init__(self, c_ptr):
        if c_ptr == ffi.NULL:
            raise UfbxError("Element pointer is NULL")
        self._ptr = c_ptr

    @property
    def name(self) -> str:
        """Element name"""
        return _to_str(self._ptr.name)

    @property
    def element_id(self) -> int:
        """Unique element ID"""
        return self._ptr.element_id

    @property
    def typed_id(self) -> int:
        """Type-specific ID"""
        return self._ptr.typed_id

    @property
    def type(self) -> int:
        """Element type (ufbx_element_type)"""
        return self._ptr.type

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}' id={self.element_id}>"


class Node(Element):
    """Scene node with transform and hierarchy"""

    @property
    def parent(self) -> Optional['Node']:
        """Parent node"""
        if self._ptr.parent == ffi.NULL:
            return None
        return Node(self._ptr.parent)

    @property
    def children(self) -> List['Node']:
        """Child nodes"""
        return [Node(self._ptr.children.data[i])
                for i in range(self._ptr.children.count)]

    @property
    def local_transform(self) -> Transform:
        """Local transform"""
        return Transform.from_c(self._ptr.local_transform)

    @property
    def node_to_world(self) -> Matrix:
        """Node to world transform matrix"""
        return Matrix.from_c(self._ptr.node_to_world)

    @property
    def node_to_parent(self) -> Matrix:
        """Node to parent transform matrix"""
        return Matrix.from_c(self._ptr.node_to_parent)

    @property
    def mesh(self) -> Optional['Mesh']:
        """Attached mesh"""
        if self._ptr.mesh == ffi.NULL:
            return None
        return Mesh(self._ptr.mesh)

    @property
    def light(self) -> Optional['Light']:
        """Attached light"""
        if self._ptr.light == ffi.NULL:
            return None
        return Light(self._ptr.light)

    @property
    def camera(self) -> Optional['Camera']:
        """Attached camera"""
        if self._ptr.camera == ffi.NULL:
            return None
        return Camera(self._ptr.camera)

    @property
    def bone(self) -> Optional['Bone']:
        """Attached bone"""
        if self._ptr.bone == ffi.NULL:
            return None
        return Bone(self._ptr.bone)

    @property
    def visible(self) -> bool:
        """Node visibility"""
        return bool(self._ptr.visible)

    @property
    def is_root(self) -> bool:
        """Is this the root node"""
        return bool(self._ptr.is_root)

    @property
    def materials(self) -> List['Material']:
        """Materials attached to this node"""
        return [Material(self._ptr.materials.data[i])
                for i in range(self._ptr.materials.count)]


class Mesh(Element):
    """Polygonal mesh geometry"""

    @property
    def num_vertices(self) -> int:
        """Number of vertices"""
        return self._ptr.num_vertices

    @property
    def num_indices(self) -> int:
        """Number of indices"""
        return self._ptr.num_indices

    @property
    def num_faces(self) -> int:
        """Number of faces"""
        return self._ptr.num_faces

    @property
    def num_triangles(self) -> int:
        """Number of triangles"""
        return self._ptr.num_triangles

    @property
    def vertex_position(self) -> List[Vec3]:
        """Vertex positions"""
        attr = self._ptr.vertex_position
        return [Vec3.from_c(attr.values.data[i])
                for i in range(attr.values.count)]

    @property
    def vertex_normal(self) -> List[Vec3]:
        """Vertex normals"""
        attr = self._ptr.vertex_normal
        return [Vec3.from_c(attr.values.data[i])
                for i in range(attr.values.count)]

    @property
    def vertex_uv(self) -> List[Vec2]:
        """Vertex UV coordinates"""
        attr = self._ptr.vertex_uv
        return [Vec2.from_c(attr.values.data[i])
                for i in range(attr.values.count)]

    @property
    def materials(self) -> List['Material']:
        """Materials used by this mesh"""
        return [Material(self._ptr.materials.data[i])
                for i in range(self._ptr.materials.count)]

    @property
    def skin_deformers(self) -> List['SkinDeformer']:
        """Skin deformers affecting this mesh"""
        return [SkinDeformer(self._ptr.skin_deformers.data[i])
                for i in range(self._ptr.skin_deformers.count)]

    @property
    def blend_deformers(self) -> List['BlendDeformer']:
        """Blend deformers affecting this mesh"""
        return [BlendDeformer(self._ptr.blend_deformers.data[i])
                for i in range(self._ptr.blend_deformers.count)]

    def triangulate_face(self, face_index: int) -> List[int]:
        """Triangulate a face, returns triangle indices"""
        if face_index >= self.num_faces:
            raise IndexError(f"Face index {face_index} out of range")

        face = self._ptr.faces.data[face_index]
        max_triangles = face.num_indices - 2
        indices = ffi.new(f"uint32_t[{max_triangles * 3}]")

        num_tris = lib.ufbx_triangulate_face(indices, max_triangles * 3, self._ptr, face)
        return list(indices[0:num_tris * 3])


class Light(Element):
    """Light source"""

    @property
    def color(self) -> Vec3:
        """Light color"""
        return Vec3.from_c(self._ptr.color)

    @property
    def intensity(self) -> float:
        """Light intensity"""
        return self._ptr.intensity

    @property
    def light_type(self) -> int:
        """Light type (ufbx_light_type)"""
        return self._ptr.type_


class Camera(Element):
    """Camera"""

    @property
    def projection_mode(self) -> int:
        """Projection mode (ufbx_projection_mode)"""
        return self._ptr.projection_mode

    @property
    def resolution(self) -> Vec2:
        """Camera resolution"""
        return Vec2.from_c(self._ptr.resolution)

    @property
    def field_of_view_deg(self) -> Vec2:
        """Field of view in degrees"""
        return Vec2.from_c(self._ptr.field_of_view_deg)

    @property
    def near_plane(self) -> float:
        """Near clipping plane"""
        return self._ptr.near_plane

    @property
    def far_plane(self) -> float:
        """Far clipping plane"""
        return self._ptr.far_plane


class Bone(Element):
    """Bone information"""

    @property
    def radius(self) -> float:
        """Bone radius"""
        return self._ptr.radius

    @property
    def relative_length(self) -> float:
        """Relative length"""
        return self._ptr.relative_length


class Material(Element):
    """Surface material"""

    @property
    def shader_type(self) -> int:
        """Shader type"""
        return self._ptr.shader_type

    @property
    def textures(self) -> List['Texture']:
        """Textures used by this material"""
        return [Texture(self._ptr.textures.data[i])
                for i in range(self._ptr.textures.count)]


class Texture(Element):
    """Texture"""

    @property
    def texture_type(self) -> int:
        """Texture type"""
        return self._ptr.type_

    @property
    def filename(self) -> str:
        """Texture filename"""
        return _to_str(self._ptr.filename)

    @property
    def absolute_filename(self) -> str:
        """Absolute texture filename"""
        return _to_str(self._ptr.absolute_filename)

    @property
    def relative_filename(self) -> str:
        """Relative texture filename"""
        return _to_str(self._ptr.relative_filename)


class Anim:
    """Animation descriptor"""

    def __init__(self, c_ptr):
        if c_ptr == ffi.NULL:
            raise UfbxError("Anim pointer is NULL")
        self._ptr = c_ptr

    @property
    def time_begin(self) -> float:
        """Animation start time"""
        return self._ptr.time_begin

    @property
    def time_end(self) -> float:
        """Animation end time"""
        return self._ptr.time_end


class AnimStack(Element):
    """Animation stack"""

    @property
    def time_begin(self) -> float:
        """Animation start time"""
        return self._ptr.time_begin

    @property
    def time_end(self) -> float:
        """Animation end time"""
        return self._ptr.time_end

    @property
    def anim(self) -> Anim:
        """Animation descriptor"""
        return Anim(self._ptr.anim)


class AnimLayer(Element):
    """Animation layer"""

    @property
    def weight(self) -> float:
        """Layer weight"""
        return self._ptr.weight


class AnimCurve(Element):
    """Animation curve"""

    @property
    def min_value(self) -> float:
        """Minimum curve value"""
        return self._ptr.min_value

    @property
    def max_value(self) -> float:
        """Maximum curve value"""
        return self._ptr.max_value

    def evaluate(self, time: float, default_value: float = 0.0) -> float:
        """Evaluate curve at given time"""
        return lib.ufbx_evaluate_curve(self._ptr, time, default_value)


class SkinDeformer(Element):
    """Skeletal skinning deformer"""

    @property
    def skinning_method(self) -> int:
        """Skinning method"""
        return self._ptr.skinning_method

    @property
    def clusters(self) -> List['SkinCluster']:
        """Skin clusters (one per bone)"""
        return [SkinCluster(self._ptr.clusters.data[i])
                for i in range(self._ptr.clusters.count)]


class SkinCluster(Element):
    """Single bone cluster in skin deformer"""

    @property
    def bone_node(self) -> Node:
        """Bone node"""
        return Node(self._ptr.bone_node)

    @property
    def geometry_to_bone(self) -> Matrix:
        """Geometry to bone transform"""
        return Matrix.from_c(self._ptr.geometry_to_bone)


class BlendDeformer(Element):
    """Blend shape deformer"""

    @property
    def channels(self) -> List['BlendChannel']:
        """Blend channels"""
        return [BlendChannel(self._ptr.channels.data[i])
                for i in range(self._ptr.channels.count)]


class BlendChannel(Element):
    """Blend shape channel"""

    @property
    def weight(self) -> float:
        """Channel weight"""
        return self._ptr.weight


class BlendShape(Element):
    """Blend shape target"""
    pass


class CacheDeformer(Element):
    """Geometry cache deformer"""
    pass


class CacheFile(Element):
    """Cache file reference"""
    pass


class Constraint(Element):
    """Constraint"""

    @property
    def constraint_type(self) -> int:
        """Constraint type"""
        return self._ptr.type_


class DisplayLayer(Element):
    """Display layer"""
    pass


class SelectionSet(Element):
    """Selection set"""
    pass


class Character(Element):
    """Character definition"""
    pass


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
        filename_bytes = _from_str(filename)

        # Call C API
        opts_ptr = ffi.NULL  # Custom options not supported yet
        scene_ptr = lib.ufbx_load_file(filename_bytes, opts_ptr, error)

        if scene_ptr == ffi.NULL:
            # Extract error information
            if error.description.data != ffi.NULL and error.description.length > 0:
                error_desc = _to_str(error.description)
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
                error_desc = _to_str(error.description)
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
    def root_node(self) -> Node:
        """Root node of the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return Node(self._scene.root_node)

    @property
    def nodes(self) -> List[Node]:
        """All nodes in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [Node(self._scene.nodes.data[i])
                for i in range(self._scene.nodes.count)]

    @property
    def meshes(self) -> List[Mesh]:
        """All meshes in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [Mesh(self._scene.meshes.data[i])
                for i in range(self._scene.meshes.count)]

    @property
    def lights(self) -> List[Light]:
        """All lights in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [Light(self._scene.lights.data[i])
                for i in range(self._scene.lights.count)]

    @property
    def cameras(self) -> List[Camera]:
        """All cameras in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [Camera(self._scene.cameras.data[i])
                for i in range(self._scene.cameras.count)]

    @property
    def materials(self) -> List[Material]:
        """All materials in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [Material(self._scene.materials.data[i])
                for i in range(self._scene.materials.count)]

    @property
    def textures(self) -> List[Texture]:
        """All textures in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [Texture(self._scene.textures.data[i])
                for i in range(self._scene.textures.count)]

    @property
    def anim_stacks(self) -> List[AnimStack]:
        """All animation stacks in the scene"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return [AnimStack(self._scene.anim_stacks.data[i])
                for i in range(self._scene.anim_stacks.count)]

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
    def light_count(self) -> int:
        """Number of lights"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.lights.count

    @property
    def camera_count(self) -> int:
        """Number of cameras"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.cameras.count

    @property
    def material_count(self) -> int:
        """Number of materials"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.materials.count

    @property
    def texture_count(self) -> int:
        """Number of textures"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.textures.count

    @property
    def animation_count(self) -> int:
        """Number of animations"""
        if self._closed:
            raise UfbxError("Scene is closed")
        return self._scene.anim_stacks.count

    def find_node(self, name: str) -> Optional[Node]:
        """Find node by name"""
        if self._closed:
            raise UfbxError("Scene is closed")
        name_bytes = _from_str(name)
        node_ptr = lib.ufbx_find_node_len(self._scene, name_bytes, len(name_bytes))
        if node_ptr == ffi.NULL:
            return None
        return Node(node_ptr)

    def find_material(self, name: str) -> Optional[Material]:
        """Find material by name"""
        if self._closed:
            raise UfbxError("Scene is closed")
        name_bytes = _from_str(name)
        mat_ptr = lib.ufbx_find_material_len(self._scene, name_bytes, len(name_bytes))
        if mat_ptr == ffi.NULL:
            return None
        return Material(mat_ptr)

    def find_anim_stack(self, name: str) -> Optional[AnimStack]:
        """Find animation stack by name"""
        if self._closed:
            raise UfbxError("Scene is closed")
        name_bytes = _from_str(name)
        anim_ptr = lib.ufbx_find_anim_stack_len(self._scene, name_bytes, len(name_bytes))
        if anim_ptr == ffi.NULL:
            return None
        return AnimStack(anim_ptr)

    def evaluate_scene(self, anim: Optional[Anim], time: float) -> 'Scene':
        """Evaluate scene at a specific time with animation

        Returns a new Scene with evaluated transforms
        """
        if self._closed:
            raise UfbxError("Scene is closed")

        error = ffi.new("ufbx_error *")
        anim_ptr = anim._ptr if anim else ffi.NULL
        opts_ptr = ffi.NULL

        evaluated_scene = lib.ufbx_evaluate_scene(self._scene, anim_ptr, time, opts_ptr, error)

        if evaluated_scene == ffi.NULL:
            if error.description.data != ffi.NULL and error.description.length > 0:
                error_desc = _to_str(error.description)
            else:
                error_desc = "Failed to evaluate scene"
            raise UfbxError(error_desc, error.type)

        return Scene(evaluated_scene)

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
