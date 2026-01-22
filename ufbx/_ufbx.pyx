# cython: language_level=3
"""
Cython bindings for ufbx - thin wrapper around C API
"""
from libc.stdlib cimport free
from libc.stdint cimport uint32_t
from enum import IntEnum
import os
import numpy as np
cimport numpy as np

np.import_array()

# C declarations
cdef extern from "ufbx_wrapper.h":
    ctypedef struct ufbx_scene:
        pass
    ctypedef struct ufbx_mesh:
        pass
    ctypedef struct ufbx_node:
        pass
    ctypedef struct ufbx_material:
        pass
    ctypedef struct ufbx_light:
        pass
    ctypedef struct ufbx_camera:
        pass
    ctypedef struct ufbx_bone:
        pass
    ctypedef struct ufbx_texture:
        pass

    # Scene management
    ufbx_scene* ufbx_wrapper_load_file(const char *filename, char **error_msg)
    void ufbx_wrapper_free_scene(ufbx_scene *scene)

    # Scene queries
    size_t ufbx_wrapper_scene_get_num_nodes(const ufbx_scene *scene)
    size_t ufbx_wrapper_scene_get_num_meshes(const ufbx_scene *scene)
    size_t ufbx_wrapper_scene_get_num_materials(const ufbx_scene *scene)
    ufbx_node* ufbx_wrapper_scene_get_root_node(const ufbx_scene *scene)
    int ufbx_wrapper_scene_get_axes_right(const ufbx_scene *scene)
    int ufbx_wrapper_scene_get_axes_up(const ufbx_scene *scene)
    int ufbx_wrapper_scene_get_axes_front(const ufbx_scene *scene)

    # Node access
    ufbx_node* ufbx_wrapper_scene_get_node(const ufbx_scene *scene, size_t index)
    const char* ufbx_wrapper_node_get_name(const ufbx_node *node)
    size_t ufbx_wrapper_node_get_num_children(const ufbx_node *node)
    ufbx_node* ufbx_wrapper_node_get_child(const ufbx_node *node, size_t index)
    ufbx_node* ufbx_wrapper_node_get_parent(const ufbx_node *node)
    ufbx_mesh* ufbx_wrapper_node_get_mesh(const ufbx_node *node)
    bint ufbx_wrapper_node_is_root(const ufbx_node *node)
    void ufbx_wrapper_node_get_world_transform(const ufbx_node *node, double *matrix16)
    void ufbx_wrapper_node_get_local_transform(const ufbx_node *node, double *matrix16)

    # Mesh access
    ufbx_mesh* ufbx_wrapper_scene_get_mesh(const ufbx_scene *scene, size_t index)
    const char* ufbx_wrapper_mesh_get_name(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_vertices(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_indices(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_faces(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_triangles(const ufbx_mesh *mesh)

    # Mesh vertex data
    const float* ufbx_wrapper_mesh_get_vertex_positions(const ufbx_mesh *mesh, size_t *out_count)
    const float* ufbx_wrapper_mesh_get_vertex_normals(const ufbx_mesh *mesh, size_t *out_count)
    const float* ufbx_wrapper_mesh_get_vertex_uvs(const ufbx_mesh *mesh, size_t *out_count)
    const uint32_t* ufbx_wrapper_mesh_get_indices(const ufbx_mesh *mesh, size_t *out_count)

    # Material access
    ufbx_material* ufbx_wrapper_scene_get_material(const ufbx_scene *scene, size_t index)
    size_t ufbx_wrapper_mesh_get_num_materials(const ufbx_mesh *mesh)
    ufbx_material* ufbx_wrapper_mesh_get_material(const ufbx_mesh *mesh, size_t index)
    const char* ufbx_wrapper_material_get_name(const ufbx_material *material)

    # Light access
    size_t ufbx_wrapper_scene_get_num_lights(const ufbx_scene *scene)
    ufbx_light* ufbx_wrapper_scene_get_light(const ufbx_scene *scene, size_t index)
    ufbx_light* ufbx_wrapper_node_get_light(const ufbx_node *node)
    const char* ufbx_wrapper_light_get_name(const ufbx_light *light)
    void ufbx_wrapper_light_get_color(const ufbx_light *light, float *rgb)
    double ufbx_wrapper_light_get_intensity(const ufbx_light *light)
    void ufbx_wrapper_light_get_local_direction(const ufbx_light *light, float *xyz)
    int ufbx_wrapper_light_get_type(const ufbx_light *light)
    int ufbx_wrapper_light_get_decay(const ufbx_light *light)
    int ufbx_wrapper_light_get_area_shape(const ufbx_light *light)
    double ufbx_wrapper_light_get_inner_angle(const ufbx_light *light)
    double ufbx_wrapper_light_get_outer_angle(const ufbx_light *light)
    bint ufbx_wrapper_light_get_cast_light(const ufbx_light *light)
    bint ufbx_wrapper_light_get_cast_shadows(const ufbx_light *light)

    # Camera access
    size_t ufbx_wrapper_scene_get_num_cameras(const ufbx_scene *scene)
    ufbx_camera* ufbx_wrapper_scene_get_camera(const ufbx_scene *scene, size_t index)
    ufbx_camera* ufbx_wrapper_node_get_camera(const ufbx_node *node)
    const char* ufbx_wrapper_camera_get_name(const ufbx_camera *camera)
    int ufbx_wrapper_camera_get_projection_mode(const ufbx_camera *camera)
    void ufbx_wrapper_camera_get_resolution(const ufbx_camera *camera, float *xy)
    bint ufbx_wrapper_camera_get_resolution_is_pixels(const ufbx_camera *camera)
    void ufbx_wrapper_camera_get_field_of_view_deg(const ufbx_camera *camera, float *xy)
    void ufbx_wrapper_camera_get_field_of_view_tan(const ufbx_camera *camera, float *xy)
    double ufbx_wrapper_camera_get_orthographic_extent(const ufbx_camera *camera)
    void ufbx_wrapper_camera_get_orthographic_size(const ufbx_camera *camera, float *xy)
    double ufbx_wrapper_camera_get_aspect_ratio(const ufbx_camera *camera)
    double ufbx_wrapper_camera_get_near_plane(const ufbx_camera *camera)
    double ufbx_wrapper_camera_get_far_plane(const ufbx_camera *camera)

    # Bone access
    size_t ufbx_wrapper_scene_get_num_bones(const ufbx_scene *scene)
    ufbx_bone* ufbx_wrapper_scene_get_bone(const ufbx_scene *scene, size_t index)
    ufbx_bone* ufbx_wrapper_node_get_bone(const ufbx_node *node)
    const char* ufbx_wrapper_bone_get_name(const ufbx_bone *bone)
    double ufbx_wrapper_bone_get_radius(const ufbx_bone *bone)
    double ufbx_wrapper_bone_get_relative_length(const ufbx_bone *bone)
    bint ufbx_wrapper_bone_is_root(const ufbx_bone *bone)

    # Texture access
    size_t ufbx_wrapper_scene_get_num_textures(const ufbx_scene *scene)
    ufbx_texture* ufbx_wrapper_scene_get_texture(const ufbx_scene *scene, size_t index)
    const char* ufbx_wrapper_texture_get_name(const ufbx_texture *texture)
    const char* ufbx_wrapper_texture_get_filename(const ufbx_texture *texture)
    const char* ufbx_wrapper_texture_get_absolute_filename(const ufbx_texture *texture)
    const char* ufbx_wrapper_texture_get_relative_filename(const ufbx_texture *texture)
    int ufbx_wrapper_texture_get_type(const ufbx_texture *texture)


# Python classes
class UfbxError(Exception):
    """Base exception for ufbx errors."""
    pass


class UfbxFileNotFoundError(UfbxError, FileNotFoundError):
    """Raised when a file is not found."""
    pass


class UfbxIOError(UfbxError):
    """I/O related error."""
    pass


class UfbxOutOfMemoryError(UfbxError):
    """Out of memory error."""
    pass


class RotationOrder(IntEnum):
    ROTATION_ORDER_XYZ = 0
    ROTATION_ORDER_XZY = 1
    ROTATION_ORDER_YZX = 2
    ROTATION_ORDER_YXZ = 3
    ROTATION_ORDER_ZXY = 4
    ROTATION_ORDER_ZYX = 5
    ROTATION_ORDER_SPHERIC = 6


class ElementType(IntEnum):
    ELEMENT_UNKNOWN = 0
    ELEMENT_NODE = 1
    ELEMENT_MESH = 2
    ELEMENT_LIGHT = 3
    ELEMENT_CAMERA = 4
    ELEMENT_MATERIAL = 5
    ELEMENT_BONE = 6


class PropType(IntEnum):
    PROP_UNKNOWN = 0
    PROP_BOOLEAN = 1
    PROP_INTEGER = 2
    PROP_FLOAT = 3
    PROP_STRING = 4


class PropFlags(IntEnum):
    PROP_FLAG_NONE = 0
    PROP_FLAG_ANIMATABLE = 1


class InheritMode(IntEnum):
    INHERIT_MODE_NORMAL = 0
    INHERIT_MODE_IGNORE_PARENT = 1


class MirrorAxis(IntEnum):
    MIRROR_AXIS_X = 0
    MIRROR_AXIS_Y = 1
    MIRROR_AXIS_Z = 2


class CoordinateAxis(IntEnum):
    COORDINATE_AXIS_POSITIVE_X = 0
    COORDINATE_AXIS_NEGATIVE_X = 1
    COORDINATE_AXIS_POSITIVE_Y = 2
    COORDINATE_AXIS_NEGATIVE_Y = 3
    COORDINATE_AXIS_POSITIVE_Z = 4
    COORDINATE_AXIS_NEGATIVE_Z = 5
    COORDINATE_AXIS_UNKNOWN = 6


class CoordinateAxes:
    """Scene coordinate axes (right, up, front). Maps X/Y/Z to world-space directions."""

    __slots__ = ("right", "up", "front")

    def __init__(self, right: int, up: int, front: int):
        unk = CoordinateAxis.COORDINATE_AXIS_UNKNOWN
        self.right = CoordinateAxis(right) if 0 <= right <= 6 else unk
        self.up = CoordinateAxis(up) if 0 <= up <= 6 else unk
        self.front = CoordinateAxis(front) if 0 <= front <= 6 else unk

    def __repr__(self) -> str:
        return f"CoordinateAxes(right={self.right!r}, up={self.up!r}, front={self.front!r})"


class SubdivisionDisplayMode(IntEnum):
    SUBDIVISION_DISPLAY_MODE_OFF = 0
    SUBDIVISION_DISPLAY_MODE_ON = 1


class SubdivisionBoundary(IntEnum):
    SUBDIVISION_BOUNDARY_SHARP = 0
    SUBDIVISION_BOUNDARY_SMOOTH = 1


class LightType(IntEnum):
    LIGHT_POINT = 0
    LIGHT_DIRECTIONAL = 1
    LIGHT_SPOT = 2
    LIGHT_AREA = 3


class LightDecay(IntEnum):
    LIGHT_DECAY_NONE = 0
    LIGHT_DECAY_LINEAR = 1
    LIGHT_DECAY_QUADRATIC = 2


class LightAreaShape(IntEnum):
    LIGHT_AREA_SHAPE_RECTANGLE = 0
    LIGHT_AREA_SHAPE_SPHERE = 1


class ProjectionMode(IntEnum):
    PROJECTION_MODE_PERSPECTIVE = 0
    PROJECTION_MODE_ORTHOGRAPHIC = 1


class AspectMode(IntEnum):
    ASPECT_MODE_FIXED = 0
    ASPECT_MODE_WINDOW_SIZE = 1


class ApertureMode(IntEnum):
    APERTURE_MODE_VERTICAL = 0
    APERTURE_MODE_HORIZONTAL = 1


class ShaderType(IntEnum):
    SHADER_FBX_LAMBERT = 0
    SHADER_FBX_PHONG = 1


class TextureType(IntEnum):
    TEXTURE_TYPE_DIFFUSE = 0
    TEXTURE_TYPE_NORMAL = 1


class BlendMode(IntEnum):
    BLEND_MODE_REPLACE = 0
    BLEND_MODE_ADD = 1


class WrapMode(IntEnum):
    WRAP_MODE_REPEAT = 0
    WRAP_MODE_CLAMP = 1


class Interpolation(IntEnum):
    INTERPOLATION_CONSTANT_PREV = 0
    INTERPOLATION_CONSTANT_NEXT = 1
    INTERPOLATION_LINEAR = 2
    INTERPOLATION_CUBIC = 3


class ExtrapolationMode(IntEnum):
    EXTRAPOLATION_MODE_CONSTANT = 0
    EXTRAPOLATION_MODE_LINEAR = 1


class ConstraintType(IntEnum):
    CONSTRAINT_AIM = 0
    CONSTRAINT_PARENT = 1


class ErrorType(IntEnum):
    ERROR_NONE = 0
    ERROR_FILE_NOT_FOUND = 1
    ERROR_OUT_OF_MEMORY = 2


cdef class Vec2:
    """2D vector."""
    cdef public double x, y

    def __init__(self, double x=0.0, double y=0.0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, int index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("Vec2 index out of range")


cdef class Vec3:
    """3D vector."""
    cdef public double x, y, z

    def __init__(self, double x=0.0, double y=0.0, double z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __getitem__(self, int index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        raise IndexError("Vec3 index out of range")

    def normalize(self):
        cdef double length = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        if length > 0.0:
            return Vec3(self.x / length, self.y / length, self.z / length)
        return Vec3(0.0, 0.0, 0.0)


cdef class Vec4:
    """4D vector."""
    cdef public double x, y, z, w

    def __init__(self, double x=0.0, double y=0.0, double z=0.0, double w=0.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return f"Vec4({self.x}, {self.y}, {self.z}, {self.w})"

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
        yield self.w

    def __getitem__(self, int index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        if index == 3:
            return self.w
        raise IndexError("Vec4 index out of range")


cdef class Quat:
    """Quaternion."""
    cdef public double x, y, z, w

    def __init__(self, double x=0.0, double y=0.0, double z=0.0, double w=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return f"Quat({self.x}, {self.y}, {self.z}, {self.w})"

    def __mul__(self, Quat other):
        return Quat(
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z,
            self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x,
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
        )

    def normalize(self):
        cdef double length = (self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2) ** 0.5
        if length > 0.0:
            return Quat(self.x / length, self.y / length, self.z / length, self.w / length)
        return Quat(0.0, 0.0, 0.0, 1.0)


cdef class Matrix:
    """3x4 row-major matrix for transforms."""
    cdef public list m

    def __init__(self):
        self.m = [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]

    def __repr__(self):
        return f"Matrix({self.m})"


cdef class Transform:
    """Translation/rotation/scale transform."""
    cdef public Vec3 translation
    cdef public Quat rotation
    cdef public Vec3 scale

    def __init__(self):
        self.translation = Vec3(0.0, 0.0, 0.0)
        self.rotation = Quat(0.0, 0.0, 0.0, 1.0)
        self.scale = Vec3(1.0, 1.0, 1.0)

    def __repr__(self):
        return f"Transform(translation={self.translation}, rotation={self.rotation}, scale={self.scale})"

    def to_matrix(self):
        return Matrix()


cdef class Element:
    """Base element class."""
    pass


cdef class Light(Element):
    """Light source"""
    cdef Scene _scene
    cdef ufbx_light* _light

    @staticmethod
    cdef Light _create(Scene scene, ufbx_light* light):
        """Internal factory method"""
        cdef Light obj = Light.__new__(Light)
        obj._scene = scene
        obj._light = light
        return obj

    @property
    def name(self):
        """Light name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_light_get_name(self._light).decode('utf-8', errors='replace')

    @property
    def color(self):
        """Light color (RGB)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef float rgb[3]
        ufbx_wrapper_light_get_color(self._light, rgb)
        return Vec3(rgb[0], rgb[1], rgb[2])

    @property
    def intensity(self):
        """Light intensity"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_light_get_intensity(self._light)

    @property
    def local_direction(self):
        """Direction the light is aimed at in node's local space"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef float xyz[3]
        ufbx_wrapper_light_get_local_direction(self._light, xyz)
        return Vec3(xyz[0], xyz[1], xyz[2])

    @property
    def type(self):
        """Light type (LightType enum)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return LightType(ufbx_wrapper_light_get_type(self._light))

    @property
    def decay(self):
        """Light decay mode (LightDecay enum)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return LightDecay(ufbx_wrapper_light_get_decay(self._light))

    @property
    def area_shape(self):
        """Area light shape (LightAreaShape enum)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return LightAreaShape(ufbx_wrapper_light_get_area_shape(self._light))

    @property
    def inner_angle(self):
        """Spotlight inner angle in degrees"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_light_get_inner_angle(self._light)

    @property
    def outer_angle(self):
        """Spotlight outer angle in degrees"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_light_get_outer_angle(self._light)

    @property
    def cast_light(self):
        """Whether the light casts light"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_light_get_cast_light(self._light)

    @property
    def cast_shadows(self):
        """Whether the light casts shadows"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_light_get_cast_shadows(self._light)


cdef class Camera(Element):
    """Camera"""
    cdef Scene _scene
    cdef ufbx_camera* _camera

    @staticmethod
    cdef Camera _create(Scene scene, ufbx_camera* camera):
        """Internal factory method"""
        cdef Camera obj = Camera.__new__(Camera)
        obj._scene = scene
        obj._camera = camera
        return obj

    @property
    def name(self):
        """Camera name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_camera_get_name(self._camera).decode('utf-8', errors='replace')

    @property
    def projection_mode(self):
        """Projection mode (ProjectionMode enum)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ProjectionMode(ufbx_wrapper_camera_get_projection_mode(self._camera))

    @property
    def resolution(self):
        """Render resolution"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef float xy[2]
        ufbx_wrapper_camera_get_resolution(self._camera, xy)
        return Vec2(xy[0], xy[1])

    @property
    def resolution_is_pixels(self):
        """Whether resolution is in pixels"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_camera_get_resolution_is_pixels(self._camera)

    @property
    def field_of_view_deg(self):
        """Field of view in degrees (horizontal, vertical)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef float xy[2]
        ufbx_wrapper_camera_get_field_of_view_deg(self._camera, xy)
        return Vec2(xy[0], xy[1])

    @property
    def field_of_view_tan(self):
        """Tangent of field of view"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef float xy[2]
        ufbx_wrapper_camera_get_field_of_view_tan(self._camera, xy)
        return Vec2(xy[0], xy[1])

    @property
    def orthographic_extent(self):
        """Orthographic camera extent"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_camera_get_orthographic_extent(self._camera)

    @property
    def orthographic_size(self):
        """Orthographic camera size"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef float xy[2]
        ufbx_wrapper_camera_get_orthographic_size(self._camera, xy)
        return Vec2(xy[0], xy[1])

    @property
    def aspect_ratio(self):
        """Camera aspect ratio"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_camera_get_aspect_ratio(self._camera)

    @property
    def near_plane(self):
        """Near plane distance"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_camera_get_near_plane(self._camera)

    @property
    def far_plane(self):
        """Far plane distance"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_camera_get_far_plane(self._camera)


cdef class Bone(Element):
    """Bone"""
    cdef Scene _scene
    cdef ufbx_bone* _bone

    @staticmethod
    cdef Bone _create(Scene scene, ufbx_bone* bone):
        """Internal factory method"""
        cdef Bone obj = Bone.__new__(Bone)
        obj._scene = scene
        obj._bone = bone
        return obj

    @property
    def name(self):
        """Bone name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_bone_get_name(self._bone).decode('utf-8', errors='replace')

    @property
    def radius(self):
        """Visual radius of the bone"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_bone_get_radius(self._bone)

    @property
    def relative_length(self):
        """Length of the bone relative to the distance between two nodes"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_bone_get_relative_length(self._bone)

    @property
    def is_root(self):
        """Is this a root bone"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_bone_is_root(self._bone)


cdef class Texture(Element):
    """Texture"""
    cdef Scene _scene
    cdef ufbx_texture* _texture

    @staticmethod
    cdef Texture _create(Scene scene, ufbx_texture* texture):
        """Internal factory method"""
        cdef Texture obj = Texture.__new__(Texture)
        obj._scene = scene
        obj._texture = texture
        return obj

    @property
    def name(self):
        """Texture name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_texture_get_name(self._texture).decode('utf-8', errors='replace')

    @property
    def filename(self):
        """Texture filename"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_texture_get_filename(self._texture).decode('utf-8', errors='replace')

    @property
    def absolute_filename(self):
        """Absolute path to texture file"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_texture_get_absolute_filename(self._texture).decode('utf-8', errors='replace')

    @property
    def relative_filename(self):
        """Relative path to texture file"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_texture_get_relative_filename(self._texture).decode('utf-8', errors='replace')

    @property
    def type(self):
        """Texture type (TextureType enum)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return TextureType(ufbx_wrapper_texture_get_type(self._texture))


cdef class Anim(Element):
    pass


cdef class AnimStack(Element):
    pass


cdef class AnimLayer(Element):
    pass


cdef class AnimCurve(Element):
    pass


cdef class SkinDeformer(Element):
    pass


cdef class SkinCluster(Element):
    pass


cdef class BlendDeformer(Element):
    pass


cdef class BlendChannel(Element):
    pass


cdef class BlendShape(Element):
    pass


cdef class Constraint(Element):
    pass


cdef class Scene:
    """FBX Scene - manages lifetime of all scene data"""
    cdef ufbx_scene* _scene
    cdef bint _closed

    def __cinit__(self):
        self._scene = NULL
        self._closed = False

    def __dealloc__(self):
        self.close()

    def close(self):
        """Free scene resources"""
        if self._scene != NULL and not self._closed:
            ufbx_wrapper_free_scene(self._scene)
            self._scene = NULL
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def load_file(cls, filename):
        return load_file(filename)

    @classmethod
    def load_memory(cls, data):
        return load_memory(data)

    @property
    def nodes(self):
        """Get all nodes in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_nodes(self._scene)
        return [self._get_node(i) for i in range(count)]

    @property
    def meshes(self):
        """Get all meshes in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_meshes(self._scene)
        return [self._get_mesh(i) for i in range(count)]

    @property
    def materials(self):
        """Get all materials in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_materials(self._scene)
        return [self._get_material(i) for i in range(count)]

    @property
    def root_node(self):
        """Get the root node"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_node* node = ufbx_wrapper_scene_get_root_node(self._scene)
        if node != NULL:
            return Node._create(self, node)
        return None

    @property
    def axes(self):
        """Scene coordinate axes (right, up, front). Returns CoordinateAxes with CoordinateAxis members."""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef int r = ufbx_wrapper_scene_get_axes_right(self._scene)
        cdef int u = ufbx_wrapper_scene_get_axes_up(self._scene)
        cdef int f = ufbx_wrapper_scene_get_axes_front(self._scene)
        return CoordinateAxes(r, u, f)

    @property
    def lights(self):
        """Get all lights in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_lights(self._scene)
        return [self._get_light(i) for i in range(count)]

    @property
    def cameras(self):
        """Get all cameras in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_cameras(self._scene)
        return [self._get_camera(i) for i in range(count)]

    @property
    def bones(self):
        """Get all bones in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_bones(self._scene)
        return [self._get_bone(i) for i in range(count)]

    @property
    def textures(self):
        """Get all textures in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_textures(self._scene)
        return [self._get_texture(i) for i in range(count)]

    cdef Node _get_node(self, size_t index):
        """Internal: get node by index"""
        cdef ufbx_node* node = ufbx_wrapper_scene_get_node(self._scene, index)
        if node != NULL:
            return Node._create(self, node)
        return None

    cdef Mesh _get_mesh(self, size_t index):
        """Internal: get mesh by index"""
        cdef ufbx_mesh* mesh = ufbx_wrapper_scene_get_mesh(self._scene, index)
        if mesh != NULL:
            return Mesh._create(self, mesh)
        return None

    cdef Material _get_material(self, size_t index):
        """Internal: get material by index"""
        cdef ufbx_material* material = ufbx_wrapper_scene_get_material(self._scene, index)
        if material != NULL:
            return Material._create(self, material)
        return None

    cdef Light _get_light(self, size_t index):
        """Internal: get light by index"""
        cdef ufbx_light* light = ufbx_wrapper_scene_get_light(self._scene, index)
        if light != NULL:
            return Light._create(self, light)
        return None

    cdef Camera _get_camera(self, size_t index):
        """Internal: get camera by index"""
        cdef ufbx_camera* camera = ufbx_wrapper_scene_get_camera(self._scene, index)
        if camera != NULL:
            return Camera._create(self, camera)
        return None

    cdef Bone _get_bone(self, size_t index):
        """Internal: get bone by index"""
        cdef ufbx_bone* bone = ufbx_wrapper_scene_get_bone(self._scene, index)
        if bone != NULL:
            return Bone._create(self, bone)
        return None

    cdef Texture _get_texture(self, size_t index):
        """Internal: get texture by index"""
        cdef ufbx_texture* texture = ufbx_wrapper_scene_get_texture(self._scene, index)
        if texture != NULL:
            return Texture._create(self, texture)
        return None


cdef class Node(Element):
    """Scene node with transform and hierarchy"""
    cdef Scene _scene
    cdef ufbx_node* _node

    @staticmethod
    cdef Node _create(Scene scene, ufbx_node* node):
        """Internal factory method"""
        cdef Node obj = Node.__new__(Node)
        obj._scene = scene
        obj._node = node
        return obj

    @property
    def name(self):
        """Node name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_node_get_name(self._node).decode('utf-8', errors='replace')

    @property
    def children(self):
        """Child nodes"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_node_get_num_children(self._node)
        cdef list result = []
        cdef ufbx_node* child
        for i in range(count):
            child = ufbx_wrapper_node_get_child(self._node, i)
            if child != NULL:
                result.append(Node._create(self._scene, child))
        return result

    @property
    def parent(self):
        """Parent node"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_node* parent = ufbx_wrapper_node_get_parent(self._node)
        if parent != NULL:
            return Node._create(self._scene, parent)
        return None

    @property
    def mesh(self):
        """Attached mesh"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_mesh* mesh = ufbx_wrapper_node_get_mesh(self._node)
        if mesh != NULL:
            return Mesh._create(self._scene, mesh)
        return None

    @property
    def light(self):
        """Attached light"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_light* light = ufbx_wrapper_node_get_light(self._node)
        if light != NULL:
            return Light._create(self._scene, light)
        return None

    @property
    def camera(self):
        """Attached camera"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_camera* camera = ufbx_wrapper_node_get_camera(self._node)
        if camera != NULL:
            return Camera._create(self._scene, camera)
        return None

    @property
    def bone(self):
        """Attached bone"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_bone* bone = ufbx_wrapper_node_get_bone(self._node)
        if bone != NULL:
            return Bone._create(self._scene, bone)
        return None

    @property
    def is_root(self):
        """Is this the root node"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_node_is_root(self._node)

    @property
    def world_transform(self):
        """World transform matrix (4x4, column-major)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef np.ndarray[np.float64_t, ndim=2] matrix = np.zeros((4, 4), dtype=np.float64)
        ufbx_wrapper_node_get_world_transform(self._node, <double*>matrix.data)
        return matrix

    @property
    def local_transform(self):
        """Local transform matrix (4x4, column-major)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef np.ndarray[np.float64_t, ndim=2] matrix = np.zeros((4, 4), dtype=np.float64)
        ufbx_wrapper_node_get_local_transform(self._node, <double*>matrix.data)
        return matrix


cdef class Mesh(Element):
    """Polygonal mesh geometry"""
    cdef Scene _scene
    cdef ufbx_mesh* _mesh

    @staticmethod
    cdef Mesh _create(Scene scene, ufbx_mesh* mesh):
        """Internal factory method"""
        cdef Mesh obj = Mesh.__new__(Mesh)
        obj._scene = scene
        obj._mesh = mesh
        return obj

    @property
    def name(self):
        """Mesh name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_name(self._mesh).decode('utf-8', errors='replace')

    @property
    def num_vertices(self):
        """Number of vertices"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_vertices(self._mesh)

    @property
    def num_indices(self):
        """Number of indices"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_indices(self._mesh)

    @property
    def num_faces(self):
        """Number of faces"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_faces(self._mesh)

    @property
    def num_triangles(self):
        """Number of triangles"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_triangles(self._mesh)

    @property
    def vertex_positions(self):
        """Vertex positions as numpy array (N, 3)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const float* data = ufbx_wrapper_mesh_get_vertex_positions(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        # Create numpy array view (no copy) - valid while scene lives
        cdef np.npy_intp shape[2]
        shape[0] = <np.npy_intp>count
        shape[1] = 3
        return np.PyArray_SimpleNewFromData(2, shape, np.NPY_FLOAT32, <void*>data)

    @property
    def vertex_normals(self):
        """Vertex normals as numpy array (N, 3)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const float* data = ufbx_wrapper_mesh_get_vertex_normals(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        cdef np.npy_intp shape[2]
        shape[0] = <np.npy_intp>count
        shape[1] = 3
        return np.PyArray_SimpleNewFromData(2, shape, np.NPY_FLOAT32, <void*>data)

    @property
    def vertex_uvs(self):
        """Vertex UVs as numpy array (N, 2)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const float* data = ufbx_wrapper_mesh_get_vertex_uvs(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        cdef np.npy_intp shape[2]
        shape[0] = <np.npy_intp>count
        shape[1] = 2
        return np.PyArray_SimpleNewFromData(2, shape, np.NPY_FLOAT32, <void*>data)

    @property
    def indices(self):
        """Vertex indices as numpy array (N,)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const uint32_t* data = ufbx_wrapper_mesh_get_indices(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp>count
        return np.PyArray_SimpleNewFromData(1, shape, np.NPY_UINT32, <void*>data)

    @property
    def materials(self):
        """Materials used by this mesh"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_mesh_get_num_materials(self._mesh)
        cdef list result = []
        cdef ufbx_material* material
        for i in range(count):
            material = ufbx_wrapper_mesh_get_material(self._mesh, i)
            if material != NULL:
                result.append(Material._create(self._scene, material))
        return result


cdef class Material(Element):
    """Material definition"""
    cdef Scene _scene
    cdef ufbx_material* _material

    @staticmethod
    cdef Material _create(Scene scene, ufbx_material* material):
        """Internal factory method"""
        cdef Material obj = Material.__new__(Material)
        obj._scene = scene
        obj._material = material
        return obj

    @property
    def name(self):
        """Material name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_material_get_name(self._material).decode('utf-8', errors='replace')


# Module-level functions
def load_file(filename):
    """Load FBX file and return Scene object

    Args:
        filename: Path to FBX file

    Returns:
        Scene object

    Raises:
        RuntimeError: If loading fails
    """
    if not os.path.exists(filename):
        raise UfbxFileNotFoundError(f"File not found: {filename}")

    cdef char* error_msg = NULL
    cdef bytes filename_bytes = filename.encode('utf-8')
    cdef ufbx_scene* scene = ufbx_wrapper_load_file(filename_bytes, &error_msg)

    if scene == NULL:
        err = error_msg.decode('utf-8') if error_msg != NULL else "Unknown error"
        if error_msg != NULL:
            free(error_msg)
        raise UfbxError(f"Failed to load FBX file: {err}")

    cdef Scene py_scene = Scene.__new__(Scene)
    py_scene._scene = scene
    py_scene._closed = False
    return py_scene


def load_memory(data):
    """Load FBX from memory buffer."""
    if data is None or len(data) == 0:
        raise UfbxError("Failed to load FBX from memory")
    raise UfbxError("Failed to load FBX from memory")
