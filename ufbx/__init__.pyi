"""
Type stubs for ufbx package
"""


# Version
__version__: str

# Core API
from ufbx.core import (
    Anim as Anim,
)
from ufbx.core import (
    AnimCurve as AnimCurve,
)
from ufbx.core import (
    AnimLayer as AnimLayer,
)
from ufbx.core import (
    AnimStack as AnimStack,
)
from ufbx.core import (
    BlendChannel as BlendChannel,
)
from ufbx.core import (
    BlendDeformer as BlendDeformer,
)
from ufbx.core import (
    BlendShape as BlendShape,
)
from ufbx.core import (
    Bone as Bone,
)
from ufbx.core import (
    CacheDeformer as CacheDeformer,
)
from ufbx.core import (
    CacheFile as CacheFile,
)
from ufbx.core import (
    Camera as Camera,
)
from ufbx.core import (
    Character as Character,
)
from ufbx.core import (
    Constraint as Constraint,
)
from ufbx.core import (
    DisplayLayer as DisplayLayer,
)
from ufbx.core import (
    Element as Element,
)
from ufbx.core import (
    Light as Light,
)
from ufbx.core import (
    Material as Material,
)
from ufbx.core import (
    Matrix as Matrix,
)
from ufbx.core import (
    Mesh as Mesh,
)
from ufbx.core import (
    Node as Node,
)
from ufbx.core import (
    Quat as Quat,
)
from ufbx.core import (
    Scene as Scene,
)
from ufbx.core import (
    SelectionSet as SelectionSet,
)
from ufbx.core import (
    SkinCluster as SkinCluster,
)
from ufbx.core import (
    SkinDeformer as SkinDeformer,
)
from ufbx.core import (
    Texture as Texture,
)
from ufbx.core import (
    Transform as Transform,
)
from ufbx.core import (
    Vec2 as Vec2,
)
from ufbx.core import (
    Vec3 as Vec3,
)
from ufbx.core import (
    Vec4 as Vec4,
)
from ufbx.core import (
    load_file as load_file,
)
from ufbx.core import (
    load_memory as load_memory,
)

# Errors
from ufbx.errors import (
    UfbxError as UfbxError,
)
from ufbx.errors import (
    UfbxFileNotFoundError as UfbxFileNotFoundError,
)
from ufbx.errors import (
    UfbxIOError as UfbxIOError,
)
from ufbx.errors import (
    UfbxOutOfMemoryError as UfbxOutOfMemoryError,
)
from ufbx.generated import (
    ApertureFormat as ApertureFormat,
)
from ufbx.generated import (
    ApertureMode as ApertureMode,
)
from ufbx.generated import (
    AspectMode as AspectMode,
)
from ufbx.generated import (
    BakedKeyFlags as BakedKeyFlags,
)
from ufbx.generated import (
    BakeStepHandling as BakeStepHandling,
)
from ufbx.generated import (
    BlendMode as BlendMode,
)
from ufbx.generated import (
    CacheDataEncoding as CacheDataEncoding,
)
from ufbx.generated import (
    CacheDataFormat as CacheDataFormat,
)
from ufbx.generated import (
    CacheFileFormat as CacheFileFormat,
)
from ufbx.generated import (
    CacheInterpretation as CacheInterpretation,
)
from ufbx.generated import (
    ConstraintAimUpType as ConstraintAimUpType,
)
from ufbx.generated import (
    ConstraintIkPoleType as ConstraintIkPoleType,
)
from ufbx.generated import (
    ConstraintType as ConstraintType,
)
from ufbx.generated import (
    CoordinateAxis as CoordinateAxis,
)
from ufbx.generated import (
    DomValueType as DomValueType,
)
from ufbx.generated import (
    ElementType as ElementType,
)
from ufbx.generated import (
    ErrorType as ErrorType,
)
from ufbx.generated import (
    EvaluateFlags as EvaluateFlags,
)
from ufbx.generated import (
    Exporter as Exporter,
)
from ufbx.generated import (
    ExtrapolationMode as ExtrapolationMode,
)
from ufbx.generated import (
    FileFormat as FileFormat,
)
from ufbx.generated import (
    GateFit as GateFit,
)
from ufbx.generated import (
    GeometryTransformHandling as GeometryTransformHandling,
)
from ufbx.generated import (
    IndexErrorHandling as IndexErrorHandling,
)
from ufbx.generated import (
    InheritMode as InheritMode,
)
from ufbx.generated import (
    InheritModeHandling as InheritModeHandling,
)
from ufbx.generated import (
    Interpolation as Interpolation,
)
from ufbx.generated import (
    LightAreaShape as LightAreaShape,
)
from ufbx.generated import (
    LightDecay as LightDecay,
)
from ufbx.generated import (
    LightType as LightType,
)
from ufbx.generated import (
    LodDisplay as LodDisplay,
)
from ufbx.generated import (
    MarkerType as MarkerType,
)
from ufbx.generated import (
    MaterialFbxMap as MaterialFbxMap,
)
from ufbx.generated import (
    MaterialFeature as MaterialFeature,
)
from ufbx.generated import (
    MaterialPbrMap as MaterialPbrMap,
)
from ufbx.generated import (
    MirrorAxis as MirrorAxis,
)
from ufbx.generated import (
    NurbsTopology as NurbsTopology,
)
from ufbx.generated import (
    OpenFileType as OpenFileType,
)
from ufbx.generated import (
    PivotHandling as PivotHandling,
)
from ufbx.generated import (
    ProgressResult as ProgressResult,
)
from ufbx.generated import (
    ProjectionMode as ProjectionMode,
)
from ufbx.generated import (
    PropFlags as PropFlags,
)
from ufbx.generated import (
    PropType as PropType,
)

# Enums
from ufbx.generated import (
    RotationOrder as RotationOrder,
)
from ufbx.generated import (
    ShaderTextureType as ShaderTextureType,
)
from ufbx.generated import (
    ShaderType as ShaderType,
)
from ufbx.generated import (
    SkinningMethod as SkinningMethod,
)
from ufbx.generated import (
    SnapMode as SnapMode,
)
from ufbx.generated import (
    SpaceConversion as SpaceConversion,
)
from ufbx.generated import (
    SubdivisionBoundary as SubdivisionBoundary,
)
from ufbx.generated import (
    SubdivisionDisplayMode as SubdivisionDisplayMode,
)
from ufbx.generated import (
    TextureType as TextureType,
)
from ufbx.generated import (
    ThumbnailFormat as ThumbnailFormat,
)
from ufbx.generated import (
    TimeMode as TimeMode,
)
from ufbx.generated import (
    TimeProtocol as TimeProtocol,
)
from ufbx.generated import (
    TopoFlags as TopoFlags,
)
from ufbx.generated import (
    TransformFlags as TransformFlags,
)
from ufbx.generated import (
    UnicodeErrorHandling as UnicodeErrorHandling,
)
from ufbx.generated import (
    WarningType as WarningType,
)
from ufbx.generated import (
    WrapMode as WrapMode,
)

__all__: list[str]
