"""
ufbx - Python bindings for ufbx FBX loader

High-performance Python bindings for the ufbx FBX file loader library
with 100% API coverage.

Basic usage:
    >>> import ufbx
    >>> with ufbx.load_file("model.fbx") as scene:
    ...     print(f"Loaded {scene.node_count} nodes")
    ...     for node in scene.nodes:
    ...         print(f"Node: {node.name}")
    ...         if node.mesh:
    ...             print(f"  Mesh with {node.mesh.num_vertices} vertices")

https://github.com/ufbx/ufbx
"""

__version__ = '0.0.0'

# Export core API
from ufbx.core import (
    # Scene
    Scene, load_file, load_memory,
    # Math types
    Vec2, Vec3, Vec4, Quat, Matrix, Transform,
    # Elements
    Element, Node, Mesh,
    # Lights and cameras
    Light, Camera, Bone,
    # Materials
    Material, Texture,
    # Animation
    Anim, AnimStack, AnimLayer, AnimCurve,
    # Deformers
    SkinDeformer, SkinCluster,
    BlendDeformer, BlendChannel, BlendShape,
    CacheDeformer, CacheFile,
    # Constraints
    Constraint,
    # Collections
    DisplayLayer, SelectionSet, Character,
)

# Export errors
from ufbx.errors import (
    UfbxError,
    UfbxFileNotFoundError,
    UfbxIOError,
    UfbxOutOfMemoryError,
)

# Export all enums from generated module
from ufbx.generated import (
    # Core enums
    RotationOrder, ElementType, PropType, PropFlags,
    # Transform and hierarchy
    InheritMode, MirrorAxis, CoordinateAxis,
    SpaceConversion, GeometryTransformHandling, InheritModeHandling, PivotHandling,
    # Geometry
    SubdivisionDisplayMode, SubdivisionBoundary, NurbsTopology, TopoFlags,
    # Lights
    LightType, LightDecay, LightAreaShape,
    # Cameras
    ProjectionMode, AspectMode, ApertureMode, GateFit, ApertureFormat,
    # Deformers
    SkinningMethod, MarkerType, LodDisplay,
    # Cache
    CacheFileFormat, CacheDataFormat, CacheDataEncoding, CacheInterpretation,
    # Materials and shaders
    ShaderType, MaterialFbxMap, MaterialPbrMap, MaterialFeature,
    TextureType, BlendMode, WrapMode, ShaderTextureType,
    # Animation
    Interpolation, ExtrapolationMode, BakedKeyFlags,
    # Constraints
    ConstraintType, ConstraintAimUpType, ConstraintIkPoleType,
    # File and metadata
    Exporter, FileFormat, WarningType, ThumbnailFormat,
    TimeMode, TimeProtocol, SnapMode,
    # Error handling
    ErrorType, ProgressResult, IndexErrorHandling, UnicodeErrorHandling,
    # Evaluation
    EvaluateFlags, BakeStepHandling, TransformFlags,
    # DOM
    DomValueType,
    # Open file type
    OpenFileType,
)

__all__ = [
    # Version
    "__version__",

    # Core classes
    "Scene",

    # Convenience functions
    "load_file",
    "load_memory",

    # Math types
    "Vec2", "Vec3", "Vec4", "Quat", "Matrix", "Transform",

    # Element types
    "Element", "Node", "Mesh",
    "Light", "Camera", "Bone",
    "Material", "Texture",
    "Anim", "AnimStack", "AnimLayer", "AnimCurve",
    "SkinDeformer", "SkinCluster",
    "BlendDeformer", "BlendChannel", "BlendShape",
    "CacheDeformer", "CacheFile",
    "Constraint",
    "DisplayLayer", "SelectionSet", "Character",

    # Exceptions
    "UfbxError",
    "UfbxFileNotFoundError",
    "UfbxOutOfMemoryError",
    "UfbxIOError",

    # Core enums
    "RotationOrder", "ElementType", "PropType", "PropFlags",
    "InheritMode", "MirrorAxis", "CoordinateAxis",
    "SpaceConversion", "GeometryTransformHandling", "InheritModeHandling", "PivotHandling",
    "SubdivisionDisplayMode", "SubdivisionBoundary", "NurbsTopology", "TopoFlags",
    "LightType", "LightDecay", "LightAreaShape",
    "ProjectionMode", "AspectMode", "ApertureMode", "GateFit", "ApertureFormat",
    "SkinningMethod", "MarkerType", "LodDisplay",
    "CacheFileFormat", "CacheDataFormat", "CacheDataEncoding", "CacheInterpretation",
    "ShaderType", "MaterialFbxMap", "MaterialPbrMap", "MaterialFeature",
    "TextureType", "BlendMode", "WrapMode", "ShaderTextureType",
    "Interpolation", "ExtrapolationMode", "BakedKeyFlags",
    "ConstraintType", "ConstraintAimUpType", "ConstraintIkPoleType",
    "Exporter", "FileFormat", "WarningType", "ThumbnailFormat",
    "TimeMode", "TimeProtocol", "SnapMode",
    "ErrorType", "ProgressResult", "IndexErrorHandling", "UnicodeErrorHandling",
    "EvaluateFlags", "BakeStepHandling", "TransformFlags",
    "DomValueType", "OpenFileType",
]
