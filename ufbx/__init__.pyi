from __future__ import annotations

from collections.abc import Iterator
from enum import IntEnum
from typing import Any

import numpy as np

__version__: str

class UfbxError(Exception): ...
class UfbxFileNotFoundError(UfbxError, FileNotFoundError): ...
class UfbxIOError(UfbxError): ...
class UfbxOutOfMemoryError(UfbxError): ...

class RotationOrder(IntEnum):
    ROTATION_ORDER_XYZ: int
    ROTATION_ORDER_XZY: int
    ROTATION_ORDER_YZX: int
    ROTATION_ORDER_YXZ: int
    ROTATION_ORDER_ZXY: int
    ROTATION_ORDER_ZYX: int
    ROTATION_ORDER_SPHERIC: int

class ElementType(IntEnum):
    ELEMENT_UNKNOWN: int
    ELEMENT_NODE: int
    ELEMENT_MESH: int
    ELEMENT_LIGHT: int
    ELEMENT_CAMERA: int
    ELEMENT_MATERIAL: int
    ELEMENT_BONE: int

class PropType(IntEnum):
    PROP_UNKNOWN: int
    PROP_BOOLEAN: int
    PROP_INTEGER: int
    PROP_FLOAT: int
    PROP_STRING: int

class PropFlags(IntEnum):
    PROP_FLAG_NONE: int
    PROP_FLAG_ANIMATABLE: int

class InheritMode(IntEnum):
    INHERIT_MODE_NORMAL: int
    INHERIT_MODE_IGNORE_PARENT: int

class MirrorAxis(IntEnum):
    MIRROR_AXIS_X: int
    MIRROR_AXIS_Y: int
    MIRROR_AXIS_Z: int

class CoordinateAxis(IntEnum):
    COORDINATE_AXIS_X: int
    COORDINATE_AXIS_Y: int
    COORDINATE_AXIS_Z: int

class SubdivisionDisplayMode(IntEnum):
    SUBDIVISION_DISPLAY_MODE_OFF: int
    SUBDIVISION_DISPLAY_MODE_ON: int

class SubdivisionBoundary(IntEnum):
    SUBDIVISION_BOUNDARY_SHARP: int
    SUBDIVISION_BOUNDARY_SMOOTH: int

class LightType(IntEnum):
    LIGHT_POINT: int
    LIGHT_DIRECTIONAL: int
    LIGHT_SPOT: int
    LIGHT_AREA: int

class LightDecay(IntEnum):
    LIGHT_DECAY_NONE: int
    LIGHT_DECAY_LINEAR: int
    LIGHT_DECAY_QUADRATIC: int

class LightAreaShape(IntEnum):
    LIGHT_AREA_SHAPE_RECTANGLE: int
    LIGHT_AREA_SHAPE_SPHERE: int

class ProjectionMode(IntEnum):
    PROJECTION_MODE_PERSPECTIVE: int
    PROJECTION_MODE_ORTHOGRAPHIC: int

class AspectMode(IntEnum):
    ASPECT_MODE_FIXED: int
    ASPECT_MODE_WINDOW_SIZE: int

class ApertureMode(IntEnum):
    APERTURE_MODE_VERTICAL: int
    APERTURE_MODE_HORIZONTAL: int

class ShaderType(IntEnum):
    SHADER_FBX_LAMBERT: int
    SHADER_FBX_PHONG: int

class TextureType(IntEnum):
    TEXTURE_TYPE_DIFFUSE: int
    TEXTURE_TYPE_NORMAL: int

class BlendMode(IntEnum):
    BLEND_MODE_REPLACE: int
    BLEND_MODE_ADD: int

class WrapMode(IntEnum):
    WRAP_MODE_REPEAT: int
    WRAP_MODE_CLAMP: int

class Interpolation(IntEnum):
    INTERPOLATION_CONSTANT_PREV: int
    INTERPOLATION_CONSTANT_NEXT: int
    INTERPOLATION_LINEAR: int
    INTERPOLATION_CUBIC: int

class ExtrapolationMode(IntEnum):
    EXTRAPOLATION_MODE_CONSTANT: int
    EXTRAPOLATION_MODE_LINEAR: int

class ConstraintType(IntEnum):
    CONSTRAINT_AIM: int
    CONSTRAINT_PARENT: int

class ErrorType(IntEnum):
    ERROR_NONE: int
    ERROR_FILE_NOT_FOUND: int
    ERROR_OUT_OF_MEMORY: int

class Vec2:
    x: float
    y: float
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None: ...
    def __iter__(self) -> Iterator[float]: ...
    def __getitem__(self, index: int) -> float: ...

class Vec3:
    x: float
    y: float
    z: float
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None: ...
    def __iter__(self) -> Iterator[float]: ...
    def __getitem__(self, index: int) -> float: ...
    def normalize(self) -> Vec3: ...

class Vec4:
    x: float
    y: float
    z: float
    w: float
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0) -> None: ...
    def __iter__(self) -> Iterator[float]: ...
    def __getitem__(self, index: int) -> float: ...

class Quat:
    x: float
    y: float
    z: float
    w: float
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0) -> None: ...
    def __mul__(self, other: Quat) -> Quat: ...
    def normalize(self) -> Quat: ...

class Matrix:
    m: list[list[float]]
    def __init__(self) -> None: ...

class Transform:
    translation: Vec3
    rotation: Quat
    scale: Vec3
    def __init__(self) -> None: ...
    def to_matrix(self) -> Matrix: ...

class Element: ...
class Light(Element): ...
class Camera(Element): ...
class Bone(Element): ...
class Texture(Element): ...
class Anim(Element): ...
class AnimStack(Element): ...
class AnimLayer(Element): ...
class AnimCurve(Element): ...
class SkinDeformer(Element): ...
class SkinCluster(Element): ...
class BlendDeformer(Element): ...
class BlendChannel(Element): ...
class BlendShape(Element): ...
class Constraint(Element): ...

class Scene:
    @classmethod
    def load_file(cls, filename: str) -> Scene: ...
    @classmethod
    def load_memory(cls, data: bytes) -> Scene: ...
    def close(self) -> None: ...
    def __enter__(self) -> Scene: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any | None) -> None: ...
    @property
    def nodes(self) -> list[Node]: ...
    @property
    def meshes(self) -> list[Mesh]: ...
    @property
    def materials(self) -> list[Material]: ...
    @property
    def root_node(self) -> Node | None: ...
    def find_node(self, name: str) -> Node | None: ...
    def find_material(self, name: str) -> Material | None: ...
    @property
    def node_count(self) -> int: ...
    @property
    def mesh_count(self) -> int: ...

class Node(Element):
    @property
    def name(self) -> str: ...
    @property
    def children(self) -> list[Node]: ...
    @property
    def parent(self) -> Node | None: ...
    @property
    def mesh(self) -> Mesh | None: ...
    @property
    def is_root(self) -> bool: ...
    @property
    def world_transform(self) -> np.ndarray[Any, Any]: ...
    @property
    def local_transform(self) -> np.ndarray[Any, Any]: ...

class Mesh(Element):
    @property
    def name(self) -> str: ...
    @property
    def num_vertices(self) -> int: ...
    @property
    def num_indices(self) -> int: ...
    @property
    def num_faces(self) -> int: ...
    @property
    def num_triangles(self) -> int: ...
    @property
    def vertex_positions(self) -> np.ndarray[Any, Any] | None: ...
    @property
    def vertex_normals(self) -> np.ndarray[Any, Any] | None: ...
    @property
    def vertex_uvs(self) -> np.ndarray[Any, Any] | None: ...
    @property
    def indices(self) -> np.ndarray[Any, Any] | None: ...
    @property
    def materials(self) -> list[Material]: ...
    def triangulate_face(self, face_index: int) -> None: ...

class Material(Element):
    @property
    def name(self) -> str: ...

def load_file(filename: str) -> Scene: ...
def load_memory(data: bytes) -> Scene: ...
