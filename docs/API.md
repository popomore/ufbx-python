# ufbx-python API Documentation

---

## Table of Contents

- [Scene.anim](#sceneanim) ❌
- [Scene.anim_curves](#sceneanim_curves) ✅
- [Scene.anim_layers](#sceneanim_layers) ❌
- [Scene.anim_stacks](#sceneanim_stacks) ✅
- [Scene.anim_values](#sceneanim_values) ❌
- [Scene.audio_clips](#sceneaudio_clips) ❌
- [Scene.audio_layers](#sceneaudio_layers) ❌
- [Scene.axes](#sceneaxes) ✅
- [Scene.blend_channels](#sceneblend_channels) ❌
- [Scene.blend_deformers](#sceneblend_deformers) ✅
- [Scene.blend_shapes](#sceneblend_shapes) ✅
- [Scene.bones](#scenebones) ✅
- [Scene.cache_deformers](#scenecache_deformers) ❌
- [Scene.cache_files](#scenecache_files) ❌
- [Scene.camera_switchers](#scenecamera_switchers) ❌
- [Scene.cameras](#scenecameras) ✅
- [Scene.characters](#scenecharacters) ❌
- [Scene.connections_dst](#sceneconnections_dst) ❌
- [Scene.connections_src](#sceneconnections_src) ❌
- [Scene.constraints](#sceneconstraints) ✅
- [Scene.display_layers](#scenedisplay_layers) ❌
- [Scene.dom_root](#scenedom_root) ❌
- [Scene.elements](#sceneelements) ❌
- [Scene.elements_by_name](#sceneelements_by_name) ❌
- [Scene.empties](#sceneempties) ✅
- [Scene.find_material()](#scenefind_material) ✅
- [Scene.find_node()](#scenefind_node) ✅
- [Scene.lights](#scenelights) ✅
- [Scene.line_curves](#sceneline_curves) ❌
- [Scene.lod_groups](#scenelod_groups) ❌
- [Scene.markers](#scenemarkers) ❌
- [Scene.materials](#scenematerials) ✅
- [Scene.meshes](#scenemeshes) ✅
- [Scene.metadata](#scenemetadata) ✅
- [Scene.metadata_objects](#scenemetadata_objects) ❌
- [Scene.nodes](#scenenodes) ✅
- [Scene.nurbs_curves](#scenenurbs_curves) ❌
- [Scene.nurbs_surfaces](#scenenurbs_surfaces) ❌
- [Scene.nurbs_trim_boundaries](#scenenurbs_trim_boundaries) ❌
- [Scene.nurbs_trim_surfaces](#scenenurbs_trim_surfaces) ❌
- [Scene.poses](#sceneposes) ❌
- [Scene.procedural_geometries](#sceneprocedural_geometries) ❌
- [Scene.root_node](#sceneroot_node) ✅
- [Scene.selection_nodes](#sceneselection_nodes) ❌
- [Scene.selection_sets](#sceneselection_sets) ❌
- [Scene.settings](#scenesettings) ✅
- [Scene.shader_bindings](#sceneshader_bindings) ❌
- [Scene.shaders](#sceneshaders) ❌
- [Scene.skin_clusters](#sceneskin_clusters) ❌
- [Scene.skin_deformers](#sceneskin_deformers) ✅
- [Scene.stereo_cameras](#scenestereo_cameras) ❌
- [Scene.texture_files](#scenetexture_files) ❌
- [Scene.textures](#scenetextures) ✅
- [Scene.unknowns](#sceneunknowns) ✅
- [Scene.videos](#scenevideos) ❌

---

## Scene Loading

```python
import ufbx

# Load from file
scene = ufbx.load_file("model.fbx")

# Load from memory
with open("model.fbx", "rb") as f:
    data = f.read()
scene = ufbx.load_memory(data)

# Context manager (auto cleanup)
with ufbx.load_file("model.fbx") as scene:
    print(f"Loaded {len(scene.nodes)} nodes")
```

---

## Scene.metadata

**Type**: `Metadata`
**Status**: ✅ Complete

Scene metadata information including version, creator, format, etc.

```python
meta = scene.metadata
print(f"FBX version: {meta.version / 1000:.1f}")  # 7.4
print(f"Creator: {meta.creator}")                 # Blender 3.6.0
print(f"Format: {'ASCII' if meta.ascii else 'Binary'}")
print(f"Filename: {meta.filename}")
```

### Metadata Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `ascii` | `bool` | Is ASCII format | ✅ |
| `version` | `int` | FBX version (e.g., 7400 = v7.4) | ✅ |
| `file_format` | `int` | File format version | ✅ |
| `creator` | `str` | Creator application | ✅ |
| `big_endian` | `bool` | Byte order | ✅ |
| `filename` | `str` | Original filename | ✅ |
| `relative_root` | `str` | Relative root path | ✅ |

---

## Scene.settings

**Type**: `SceneSettings`
**Status**: ✅ Complete

Scene settings and configuration including units, FPS, coordinate axes.

```python
settings = scene.settings
fps = settings.frames_per_second       # 24.0
units = settings.unit_meters           # 0.01 (centimeters)
axes = settings.axes                   # Coordinate axes
ambient = settings.ambient_color       # (r, g, b)
```

### SceneSettings Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `axes` | `CoordinateAxes` | Coordinate system axes | ✅ |
| `unit_meters` | `float` | Units in meters (0.01 = cm) | ✅ |
| `frames_per_second` | `float` | Frame rate | ✅ |
| `ambient_color` | `tuple[float, float, float]` | Ambient light color RGB | ✅ |
| `default_camera` | `str` | Default camera name | ✅ |
| `time_mode` | `int` | Time mode | ✅ |
| `time_protocol` | `int` | Time protocol | ✅ |
| `snap_mode` | `int` | Snap mode | ✅ |
| `original_axis_up` | `int` | Original up axis | ✅ |
| `original_unit_meters` | `float` | Original unit scale | ✅ |

---

## Scene.root_node

**Type**: `Node | None`
**Status**: ✅ Complete

Root node of scene hierarchy. All other nodes are children or descendants.

```python
root = scene.root_node
if root:
    print(f"Root node: {root.name}")
    print(f"Direct children: {len(root.children)}")

    # Traverse hierarchy
    def print_hierarchy(node, indent=0):
        print("  " * indent + node.name)
        for child in node.children:
            print_hierarchy(child, indent + 1)

    print_hierarchy(root)
```

**See**: [Node Properties](#node-properties)

---

## Scene.anim

**Type**: `Anim | None`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

Default animation descriptor for the scene.

```python
# Not yet available
# if scene.anim:
#     print(f"Default animation: {scene.anim.name}")
```

### Anim Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Animation name | ❌ |
| `layers` | `list[AnimLayer]` | Animation layers | ❌ |
| `time_begin` | `float` | Start time | ❌ |
| `time_end` | `float` | End time | ❌ |

---

## Scene.unknowns

**Type**: `list[Unknown]`
**Status**: ✅ Complete

List of elements that ufbx parsed but doesn't have specific handlers for.

```python
if scene.unknowns:
    print(f"Unknown elements: {len(scene.unknowns)}")
    for unknown in scene.unknowns:
        print(f"  {unknown.name}")
```

### Unknown Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Unknown element name | ✅ |

---

## Scene.nodes

**Type**: `list[Node]`
**Status**: ✅ Complete

Flat list of all nodes in the scene, regardless of hierarchy.

```python
print(f"Total nodes: {len(scene.nodes)}")

# Find nodes with meshes
mesh_nodes = [n for n in scene.nodes if n.mesh]
print(f"Mesh nodes: {len(mesh_nodes)}")

# Find by name
cube = next((n for n in scene.nodes if n.name == "Cube"), None)
```

### Node Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Node name | ✅ |
| `parent` | `Node \| None` | Parent node | ✅ |
| `children` | `list[Node]` | Child nodes | ✅ |
| `mesh` | `Mesh \| None` | Associated mesh | ✅ |
| `light` | `Light \| None` | Associated light | ✅ |
| `camera` | `Camera \| None` | Associated camera | ✅ |
| `bone` | `Bone \| None` | Associated bone | ✅ |
| `is_root` | `bool` | Is root node | ✅ |
| `local_transform` | `ndarray` | Local transform matrix (4x4) | ✅ |
| `world_transform` | `ndarray` | World transform matrix (4x4) | ✅ |
| `geometry_transform` | `Transform` | Geometry transform | ❌ 🟡 |
| `node_to_world` | `Matrix` | Node to world matrix | ❌ 🔴 |
| `node_to_parent` | `Matrix` | Node to parent matrix | ❌ 🟡 |
| `attrib_type` | `ElementType` | Attribute type | ❌ 🟢 |
| `inherit_mode` | `InheritMode` | Transform inherit mode | ❌ 🟡 |
| `visible` | `bool` | Visibility flag | ❌ 🟡 |
| `euler_rotation` | `Vec3` | Euler angles | ❌ 🟡 |

---

## Scene.meshes

**Type**: `list[Mesh]`
**Status**: ✅ Complete

List of all mesh geometry objects.

```python
print(f"Total meshes: {len(scene.meshes)}")

for mesh in scene.meshes:
    print(f"Mesh: {mesh.name}")
    print(f"  Vertices: {mesh.num_vertices}")
    print(f"  Triangles: {mesh.num_triangles}")
    print(f"  Materials: {len(mesh.materials)}")

    # Access vertex data
    positions = mesh.vertex_positions  # (N, 3) numpy array
    normals = mesh.vertex_normals      # (N, 3) numpy array
    uvs = mesh.vertex_uvs              # (N, 2) numpy array
```

### Mesh Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Mesh name | ✅ |
| `num_vertices` | `int` | Vertex count | ✅ |
| `num_indices` | `int` | Index count | ✅ |
| `num_faces` | `int` | Face count | ✅ |
| `num_triangles` | `int` | Triangle count | ✅ |
| `vertex_positions` | `ndarray \| None` | Vertex positions (N, 3) | ✅ |
| `vertex_normals` | `ndarray \| None` | Vertex normals (N, 3) | ✅ |
| `vertex_uvs` | `ndarray \| None` | UV coordinates (N, 2) | ✅ |
| `indices` | `ndarray \| None` | Vertex indices | ✅ |
| `materials` | `list[Material]` | Material list | ✅ |
| `vertex_tangent` | `ndarray` | Tangent vectors (N, 3) | ❌ 🔴🔴 |
| `vertex_bitangent` | `ndarray` | Bitangent vectors (N, 3) | ❌ 🔴🔴 |
| `vertex_color` | `ndarray` | Vertex colors (N, 4) | ❌ 🔴 |
| `faces` | `list[Face]` | Face data | ❌ 🟡 |
| `face_material` | `list[int]` | Face material indices | ❌ 🟡 |
| `skin_deformers` | `list[SkinDeformer]` | Skin deformers | ❌ 🟡 |
| `blend_deformers` | `list[BlendDeformer]` | Blend deformers | ❌ 🟡 |
| `edge_crease` | `list[float]` | Edge sharpness | ❌ 🟢 |
| `vertex_crease` | `list[float]` | Vertex sharpness | ❌ 🟢 |

> ⚠️ **Critical**: `vertex_tangent` and `vertex_bitangent` are required for normal mapping!

---

## Scene.materials

**Type**: `list[Material]`
**Status**: ✅ Complete

List of all material definitions (100% complete PBR and FBX support).

```python
print(f"Total materials: {len(scene.materials)}")

for material in scene.materials:
    print(f"Material: {material.name}")

    # Check features
    if material.features.pbr:
        print("  PBR material")

    # Access PBR properties
    base = material.pbr_base_color
    if base.has_value:
        r, g, b, a = base.value_vec4
        print(f"  Base color: RGB({r:.2f}, {g:.2f}, {b:.2f})")
    if base.texture:
        print(f"  Base texture: {base.texture.filename}")
```

### Material Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Material name | ✅ |
| `shader_type` | `ShaderType` | Shader type | ✅ |
| `shading_model_name` | `str` | Shading model name | ✅ |
| `features` | `MaterialFeatures` | Feature flags (23 bools) | ✅ |
| `textures` | `list[MaterialTexture]` | Texture mappings | ✅ |

### Material PBR Properties (47 total)

All properties return `MaterialMap` objects with `value_vec4`, `texture`, `has_value`, etc.

**Base**:
- `pbr_base_factor`, `pbr_base_color`

**Surface**:
- `pbr_roughness`, `pbr_metalness`, `pbr_diffuse_roughness`
- `pbr_specular_factor`, `pbr_specular_color`, `pbr_specular_ior`
- `pbr_specular_anisotropy`, `pbr_specular_rotation`

**Transmission**:
- `pbr_transmission_factor`, `pbr_transmission_color`
- `pbr_transmission_depth`, `pbr_transmission_scatter`
- `pbr_transmission_dispersion`, `pbr_transmission_roughness`, `pbr_transmission_priority`

**Subsurface**:
- `pbr_subsurface_factor`, `pbr_subsurface_color`, `pbr_subsurface_radius`
- `pbr_subsurface_scale`, `pbr_subsurface_anisotropy`, `pbr_subsurface_tint_color`
- `pbr_subsurface_type`

**Sheen**:
- `pbr_sheen_factor`, `pbr_sheen_color`, `pbr_sheen_roughness`

**Coat**:
- `pbr_coat_factor`, `pbr_coat_color`, `pbr_coat_roughness`
- `pbr_coat_ior`, `pbr_coat_anisotropy`, `pbr_coat_rotation`
- `pbr_coat_normal`, `pbr_coat_affect_base_color`, `pbr_coat_affect_base_roughness`

**Thin Film**:
- `pbr_thin_film_thickness`, `pbr_thin_film_ior`

**Emission**:
- `pbr_emission_factor`, `pbr_emission_color`

**Opacity**:
- `pbr_opacity`

**Maps**:
- `pbr_normal_map`, `pbr_tangent_map`, `pbr_displacement_map`
- `pbr_ambient_occlusion`

**Other**:
- `pbr_matte_factor`, `pbr_matte_color`
- `pbr_indirect_diffuse`, `pbr_indirect_specular`
- `pbr_glossiness`, `pbr_coat_glossiness`, `pbr_transmission_glossiness`

### Material FBX Properties (21 total)

**Diffuse**:
- `fbx_diffuse_factor`, `fbx_diffuse_color`

**Specular**:
- `fbx_specular_factor`, `fbx_specular_color`, `fbx_specular_exponent`

**Reflection**:
- `fbx_reflection_factor`, `fbx_reflection_color`

**Transparency**:
- `fbx_transparency_factor`, `fbx_transparency_color`

**Emission**:
- `fbx_emission_factor`, `fbx_emission_color`

**Ambient**:
- `fbx_ambient_factor`, `fbx_ambient_color`

**Maps**:
- `fbx_normal_map`, `fbx_bump`, `fbx_bump_factor`
- `fbx_displacement_factor`, `fbx_displacement`
- `fbx_vector_displacement_factor`, `fbx_vector_displacement`

### MaterialMap Properties

Each material property (e.g., `pbr_base_color`) returns a `MaterialMap` object:

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `value_vec4` | `tuple[float, float, float, float]` | RGBA value | ✅ |
| `value_int` | `int` | Integer value | ✅ |
| `has_value` | `bool` | Has value set | ✅ |
| `texture` | `Texture \| None` | Associated texture | ✅ |
| `texture_enabled` | `bool` | Texture enabled | ✅ |
| `feature_disabled` | `bool` | Feature disabled | ✅ |
| `value_components` | `int` | Component count (1-4) | ✅ |

### MaterialFeatures Properties

Quick boolean flags for material features:

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `pbr` | `bool` | Is PBR material | ✅ |
| `metalness` | `bool` | Has metalness | ✅ |
| `diffuse` | `bool` | Has diffuse | ✅ |
| `specular` | `bool` | Has specular | ✅ |
| `emission` | `bool` | Has emission | ✅ |
| `transmission` | `bool` | Has transmission | ✅ |
| `coat` | `bool` | Has clear coat | ✅ |
| `sheen` | `bool` | Has sheen | ✅ |
| `opacity` | `bool` | Has opacity | ✅ |
| `ambient_occlusion` | `bool` | Has AO | ✅ |
| `matte` | `bool` | Has matte | ✅ |
| `unlit` | `bool` | Is unlit | ✅ |
| `ior` | `bool` | Has IOR | ✅ |
| `diffuse_roughness` | `bool` | Has diffuse roughness | ✅ |
| `transmission_roughness` | `bool` | Has transmission roughness | ✅ |
| `thin_walled` | `bool` | Is thin walled | ✅ |
| `caustics` | `bool` | Has caustics | ✅ |
| `exit_to_background` | `bool` | Exit to background | ✅ |
| `internal_reflections` | `bool` | Has internal reflections | ✅ |
| `double_sided` | `bool` | Is double sided | ✅ |
| `roughness` | `bool` | Has roughness | ✅ |
| `glossiness` | `bool` | Has glossiness | ✅ |
| `coat_roughness` | `bool` | Has coat roughness | ✅ |

### MaterialTexture Properties

Material-texture mapping relationship:

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `material_prop` | `str` | Material property name | ✅ |
| `shader_prop` | `str` | Shader property name | ✅ |
| `texture` | `Texture \| None` | Texture object | ✅ |

---

## Scene.textures

**Type**: `list[Texture]`
**Status**: ✅ Complete (33% - basic properties only)

List of all texture objects referenced in the scene.

```python
print(f"Total textures: {len(scene.textures)}")

for texture in scene.textures:
    print(f"Texture: {texture.name}")
    print(f"  Type: {texture.type}")
    print(f"  File: {texture.filename}")
```

### Texture Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Texture name | ✅ |
| `type` | `TextureType` | Texture type | ✅ |
| `filename` | `str` | Filename | ✅ |
| `absolute_filename` | `str` | Absolute path | ✅ |
| `relative_filename` | `str` | Relative path | ✅ |
| `content` | `bytes` | Embedded texture data | ❌ 🔴 |
| `has_file` | `bool` | Has external file | ❌ 🟡 |
| `file_index` | `int` | File index | ❌ 🟡 |
| `video` | `Video \| None` | Video reference | ❌ 🟡 |
| `layers` | `list[TextureLayer]` | Texture layers | ❌ 🟢 |
| `uv_set` | `str` | UV set name | ❌ 🟡 |
| `wrap_u` | `WrapMode` | U wrap mode | ❌ 🟡 |
| `wrap_v` | `WrapMode` | V wrap mode | ❌ 🟡 |
| `uv_transform` | `Transform` | UV transform | ❌ 🟢 |
| `shader` | `Shader \| None` | Shader reference | ❌ 🟢 |

---

## Scene.videos

**Type**: `list[Video]`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

List of video texture objects.

```python
# Not yet available
# for video in scene.videos:
#     print(f"Video: {video.name}")
```

### Video Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Video name | ❌ |
| `filename` | `str` | Relative filename | ❌ |
| `absolute_filename` | `str` | Absolute filename | ❌ |
| `relative_filename` | `str` | Relative filename | ❌ |
| `raw_filename` | `bytes` | Raw filename (non-UTF-8) | ❌ |
| `raw_absolute_filename` | `bytes` | Raw absolute filename | ❌ |
| `raw_relative_filename` | `bytes` | Raw relative filename | ❌ |
| `content` | `bytes` | Embedded video content | ❌ |

---

## Scene.shaders

**Type**: `list[Shader]`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

List of shader objects referenced in materials.

```python
# Not yet available
# for shader in scene.shaders:
#     print(f"Shader: {shader.name}")
```

### Shader Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Shader name | ❌ |
| `type` | `ShaderType` | Shader type | ❌ |
| `bindings` | `list[ShaderBinding]` | Shader bindings | ❌ |

---

## Scene.shader_bindings

**Type**: `list[ShaderBinding]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of shader binding objects.

```python
# Not yet available
# for binding in scene.shader_bindings:
#     print(f"Binding: {binding.name}")
```

### ShaderBinding Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Binding name | ❌ |
| `prop_bindings` | `list[ShaderPropBinding]` | Property bindings | ❌ |

---

## Scene.lights

**Type**: `list[Light]`
**Status**: ✅ Complete

List of all light objects (point, spot, directional, area).

```python
print(f"Total lights: {len(scene.lights)}")

for light in scene.lights:
    print(f"Light: {light.name}")
    # Additional light properties available
```

---

## Scene.cameras

**Type**: `list[Camera]`
**Status**: ✅ Complete

List of all camera objects.

```python
print(f"Total cameras: {len(scene.cameras)}")

for camera in scene.cameras:
    print(f"Camera: {camera.name}")
    # Additional camera properties available
```

---

## Scene.bones

**Type**: `list[Bone]`
**Status**: ✅ Complete

List of all bone objects used for skeletal animation.

```python
print(f"Total bones: {len(scene.bones)}")

for bone in scene.bones:
    print(f"Bone: {bone.name}")
    # Additional bone properties available
```

---

## Scene.empties

**Type**: `list[Empty]`
**Status**: ✅ Complete

List of empty objects (locators), often used as control objects.

```python
print(f"Total empties: {len(scene.empties)}")

for empty in scene.empties:
    print(f"Empty: {empty.name}")
```

### Empty Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Empty object name | ✅ |

---

## Scene.line_curves

**Type**: `list[LineCurve]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of line curve objects.

```python
# Not yet available
```

### LineCurve Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Curve name | ❌ |
| `control_points` | `list[Vec3]` | Control points | ❌ |

---

## Scene.nurbs_curves

**Type**: `list[NurbsCurve]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of NURBS curve objects.

```python
# Not yet available
```

### NurbsCurve Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | NURBS curve name | ❌ |
| `control_points` | `list[Vec4]` | Control points | ❌ |
| `knot_vector` | `list[float]` | Knot vector | ❌ |

---

## Scene.nurbs_surfaces

**Type**: `list[NurbsSurface]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of NURBS surface objects.

```python
# Not yet available
```

### NurbsSurface Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | NURBS surface name | ❌ |
| `control_points` | `ndarray` | Control points grid | ❌ |
| `knot_vector_u` | `list[float]` | U knot vector | ❌ |
| `knot_vector_v` | `list[float]` | V knot vector | ❌ |

---

## Scene.nurbs_trim_surfaces

**Type**: `list[NurbsTrimSurface]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of NURBS trimmed surface objects.

```python
# Not yet available
```

### NurbsTrimSurface Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Trim surface name | ❌ |

---

## Scene.nurbs_trim_boundaries

**Type**: `list[NurbsTrimBoundary]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of NURBS trim boundary objects.

```python
# Not yet available
```

### NurbsTrimBoundary Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Trim boundary name | ❌ |

---

## Scene.procedural_geometries

**Type**: `list[ProceduralGeometry]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of procedural geometry objects.

```python
# Not yet available
```

### ProceduralGeometry Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Geometry name | ❌ |

---

## Scene.stereo_cameras

**Type**: `list[StereoCamera]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of stereo camera rig objects.

```python
# Not yet available
```

### StereoCamera Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Stereo camera name | ❌ |
| `left` | `Camera \| None` | Left camera | ❌ |
| `right` | `Camera \| None` | Right camera | ❌ |

---

## Scene.camera_switchers

**Type**: `list[CameraSwitcher]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of camera switcher objects.

```python
# Not yet available
```

### CameraSwitcher Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Camera switcher name | ❌ |

---

## Scene.markers

**Type**: `list[Marker]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of marker objects.

```python
# Not yet available
```

### Marker Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Marker name | ❌ |

---

## Scene.lod_groups

**Type**: `list[LodGroup]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of LOD (Level of Detail) group objects.

```python
# Not yet available
```

### LodGroup Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | LOD group name | ❌ |
| `lod_levels` | `list[LodLevel]` | LOD levels | ❌ |

---

## Scene.skin_deformers

**Type**: `list[CacheFile]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of cache file references (Alembic, etc.).

```python
# Not yet available
```

---

## Scene.cache_deformers

**Type**: `list[CacheDeformer]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of cache-based deformer objects.

```python
# Not yet available
```

---

## Scene.display_layers

**Type**: `list[DisplayLayer]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of display layer objects for visibility management.

```python
# Not yet available
```

### DisplayLayer Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Layer name | ❌ |
| `visible` | `bool` | Layer visibility | ❌ |
| `ui_color` | `Vec3` | UI display color | ❌ |

---

## Scene.selection_sets

**Type**: `list[SelectionSet]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of selection set objects.

```python
# Not yet available
```

### SelectionSet Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Selection set name | ❌ |
| `nodes` | `list[SelectionNode]` | Selected nodes | ❌ |

---

## Scene.selection_nodes

**Type**: `list[SelectionNode]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of selection node objects.

```python
# Not yet available
```

### SelectionNode Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Selection node name | ❌ |
| `target_node` | `Node \| None` | Target node | ❌ |

---

## Scene.characters

**Type**: `list[Character]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of character objects for animation.

```python
# Not yet available
```

### Character Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Character name | ❌ |

---

## Scene.audio_layers

**Type**: `list[AudioLayer]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of audio layer objects.

```python
# Not yet available
```

### AudioLayer Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Audio layer name | ❌ |
| `clips` | `list[AudioClip]` | Audio clips | ❌ |

---

## Scene.audio_clips

**Type**: `list[AudioClip]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of audio clip objects.

```python
# Not yet available
```

### AudioClip Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Audio clip name | ❌ |
| `filename` | `str` | Audio filename | ❌ |
| `absolute_filename` | `str` | Absolute path | ❌ |
| `relative_filename` | `str` | Relative path | ❌ |

---

## Scene.poses

**Type**: `list[Pose]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of pose data for bind poses.

```python
# Not yet available
```

### Pose Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Pose name | ❌ |
| `bind_pose` | `bool` | Is bind pose | ❌ |
| `bone_poses` | `list[BonePose]` | Bone transformations | ❌ |

---

## Scene.metadata_objects

**Type**: `list[MetadataObject]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of metadata objects attached to elements.

```python
# Not yet available
```

### MetadataObject Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Metadata object name | ❌ |

---

## Scene.texture_files

**Type**: `list[TextureFile]`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

Unique texture files referenced by the scene (deduplicated texture paths).

```python
# Not yet available
# for tex_file in scene.texture_files:
#     print(f"Texture file: {tex_file.filename}")
```

### TextureFile Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `filename` | `str` | Filename | ❌ |
| `absolute_filename` | `str` | Absolute path | ❌ |
| `relative_filename` | `str` | Relative path | ❌ |
| `index` | `int` | File index | ❌ |
| `content` | `bytes` | Embedded content | ❌ |

---

## Scene.elements

**Type**: `list[Element]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

All elements in the whole file, sorted by ID.

```python
# Not yet available
# for element in scene.elements:
#     print(f"Element: {element.name} (type: {element.type})")
```

### Element Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Element name | ❌ |
| `type` | `ElementType` | Element type | ❌ |
| `element_id` | `int` | Unique element ID | ❌ |
| `typed_id` | `int` | Type-specific ID | ❌ |

---

## Scene.connections_src

**Type**: `list[Connection]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

All connections sorted by source element.

```python
# Not yet available
# for conn in scene.connections_src:
#     # Access connection data
#     pass
```

### Connection Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `src` | `Element \| None` | Source element | ❌ |
| `dst` | `Element \| None` | Destination element | ❌ |
| `src_prop` | `str` | Source property | ❌ |
| `dst_prop` | `str` | Destination property | ❌ |

---

## Scene.connections_dst

**Type**: `list[Connection]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

All connections sorted by destination element.

```python
# Not yet available
# for conn in scene.connections_dst:
#     # Access connection data
#     pass
```

### Connection Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `src` | `Element \| None` | Source element | ❌ |
| `dst` | `Element \| None` | Destination element | ❌ |
| `src_prop` | `str` | Source property | ❌ |
| `dst_prop` | `str` | Destination property | ❌ |

---

## Scene.elements_by_name

**Type**: `list[NameElement]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

Elements sorted by name and type for efficient lookup.

```python
# Not yet available
```

### NameElement Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Element name | ❌ |
| `type` | `ElementType` | Element type | ❌ |
| `element` | `Element` | Element reference | ❌ |

---

## Scene.dom_root

**Type**: `DomNode | None`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

DOM root node (enabled if `retain_dom` load option is set).

```python
# Not yet available
# if scene.dom_root:
#     # Access DOM tree
#     pass
```

### DomNode Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Node name | ❌ |
| `children` | `list[DomNode]` | Child nodes | ❌ |
| `values` | `list[DomValue]` | Node values | ❌ |

---

## Scene.axes

**Type**: `list[AnimStack]`
**Status**: ✅ Complete

List of animation stacks (animation takes/clips).

```python
print(f"Animation stacks: {len(scene.anim_stacks)}")

for stack in scene.anim_stacks:
    print(f"Anim stack: {stack.name}")
    # Additional animation properties available
```

---

## Scene.anim_layers

**Type**: `list[AnimLayer]`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

List of animation layers within animation stacks.

```python
# Not yet available
# for layer in scene.anim_layers:
#     print(f"Anim layer: {layer.name}")
```

### AnimLayer Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Layer name | ❌ |
| `weight` | `float` | Layer weight | ❌ |
| `anim_values` | `list[AnimValue]` | Animation values | ❌ |
| `blended` | `bool` | Is blended | ❌ |
| `additive` | `bool` | Is additive | ❌ |

---

## Scene.anim_values

**Type**: `list[AnimValue]`
**Status**: ❌ Not Implemented
**Priority**: 🟢 Low

List of animation values.

```python
# Not yet available
# for value in scene.anim_values:
#     # Access animation value data
#     pass
```

### AnimValue Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Value name | ❌ |
| `default_value` | `float \| Vec3` | Default value | ❌ |
| `curves` | `list[AnimCurve]` | Animation curves | ❌ |

---

## Scene.anim_curves

**Type**: `list[AnimCurve]`
**Status**: ✅ Complete

List of all animation curves (keyframe data).

```python
print(f"Animation curves: {len(scene.anim_curves)}")

for curve in scene.anim_curves:
    # Access keyframe data
    pass
```

---

## Scene.skin_deformers

**Type**: `list[SkinDeformer]`
**Status**: ✅ Complete

List of skin deformers used for skeletal animation.

```python
print(f"Skin deformers: {len(scene.skin_deformers)}")

for deformer in scene.skin_deformers:
    print(f"Skin: {deformer.name}")
    # Access bone weights
```

---

## Scene.skin_clusters

**Type**: `list[SkinCluster]`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

List of skin clusters (bone weight information).

```python
# Not yet available
# for cluster in scene.skin_clusters:
#     print(f"Cluster: {cluster.name}")
```

### SkinCluster Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Cluster name | ❌ |
| `bone_node` | `Node \| None` | Bone node | ❌ |
| `vertices` | `list[int]` | Affected vertices | ❌ |
| `weights` | `list[float]` | Vertex weights | ❌ |
| `bind_matrix` | `Matrix` | Bind transform matrix | ❌ |

---

## Scene.blend_deformers

**Type**: `list[BlendDeformer]`
**Status**: ✅ Complete

List of blend shape deformers used for morph/shape key animation.

```python
print(f"Blend deformers: {len(scene.blend_deformers)}")

for deformer in scene.blend_deformers:
    print(f"Blend: {deformer.name}")
    # Access blend channels
```

---

## Scene.blend_channels

**Type**: `list[BlendChannel]`
**Status**: ❌ Not Implemented
**Priority**: 🟡 Medium

List of blend channels (morph targets within blend deformers).

```python
# Not yet available
# for channel in scene.blend_channels:
#     print(f"Channel: {channel.name}")
```

### BlendChannel Properties (Not Implemented)

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `name` | `str` | Channel name | ❌ |
| `weight` | `float` | Current weight | ❌ |
| `keyframes` | `list[BlendKeyframe]` | Keyframe data | ❌ |

---

## Scene.blend_shapes

**Type**: `list[BlendShape]`
**Status**: ✅ Complete

List of individual blend shapes (morph targets).

```python
print(f"Blend shapes: {len(scene.blend_shapes)}")

for shape in scene.blend_shapes:
    print(f"Shape: {shape.name}")
    # Access shape geometry
```

---

## Scene.constraints

**Type**: `list[Constraint]`
**Status**: ✅ Complete

List of constraints (parent, aim, IK, etc.).

```python
print(f"Constraints: {len(scene.constraints)}")

for constraint in scene.constraints:
    print(f"Constraint: {constraint.name}")
    # Access constraint parameters
```

---

## Scene.axes

**Type**: `CoordinateAxes`
**Status**: ✅ Complete

The coordinate system used by the scene.

```python
axes = scene.axes
print(f"Right: {axes.right}")   # 0=+X, 1=+Y, 2=+Z, etc.
print(f"Up: {axes.up}")
print(f"Front: {axes.front}")

# Common coordinate systems:
# Y-up, Z-front (Blender, Maya): right=0(+X), up=2(+Z), front=1(+Y)
# Z-up, Y-front (3ds Max):       right=0(+X), up=2(+Z), front=1(-Y)
```

### CoordinateAxes Properties

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `right` | `CoordinateAxis` | Right axis direction | ✅ |
| `up` | `CoordinateAxis` | Up axis direction | ✅ |
| `front` | `CoordinateAxis` | Front axis direction | ✅ |

---

## Scene.find_node()

**Signature**: `find_node(name: str) -> Node | None`
**Status**: ✅ Complete

Convenience method to find a node by its name.

```python
cube = scene.find_node("Cube")
if cube:
    print(f"Found node: {cube.name}")
    if cube.mesh:
        print(f"Has mesh with {cube.mesh.num_vertices} vertices")
else:
    print("Node not found")
```

---

## Scene.find_material()

**Signature**: `find_material(name: str) -> Material | None`
**Status**: ✅ Complete

Convenience method to find a material by its name.

```python
material = scene.find_material("Material.001")
if material:
    print(f"Found material: {material.name}")
    if material.features.pbr:
        print("Is PBR material")
else:
    print("Material not found")
```

---

## Helper Classes

### Transform Class ✅

3D transform (translation, rotation, scale).

| Property | Type | Description | Status |
|----------|------|-------------|--------|
| `translation` | `Vec3` | Position | ✅ |
| `rotation` | `Quat` | Rotation (quaternion) | ✅ |
| `scale` | `Vec3` | Scale | ✅ |

```python
transform = Transform()
transform.translation = Vec3(1.0, 2.0, 3.0)
transform.rotation = Quat(0, 0, 0, 1)
transform.scale = Vec3(1.0, 1.0, 1.0)

matrix = transform.to_matrix()
```

### Math Classes ✅

- `Vec2(x, y)` - 2D vector
- `Vec3(x, y, z)` - 3D vector
- `Vec4(x, y, z, w)` - 4D vector
- `Quat(x, y, z, w)` - Quaternion
- `Matrix()` - 4x4 matrix

---

## Implementation Status Summary

### By Module

| Module | Implemented | Missing | Completion |
|--------|-------------|---------|------------|
| **Material** | 79 / 79 | 0 | 100% ✅ |
| **MaterialMap** | 7 / 7 | 0 | 100% ✅ |
| **MaterialFeatures** | 23 / 23 | 0 | 100% ✅ |
| **MaterialTexture** | 3 / 3 | 0 | 100% ✅ |
| **Texture** | 5 / 15 | 10 | 33% ⚠️ |
| **Scene (Core)** | 21 / 40 | 19 | 53% ⚠️ |
| **Node** | 10 / 17 | 7 | 59% ⚠️ |
| **Mesh** | 10 / 19 | 9 | 53% ⚠️ |

### Critical Missing Features

**🔴 Critical Priority** (Required for normal mapping):
1. `Mesh.vertex_tangent` - Tangent vectors for TBN matrix
2. `Mesh.vertex_bitangent` - Bitangent vectors for TBN matrix
3. `Mesh.vertex_color` - Vertex color data
4. `Texture.content` - Embedded texture data

**🔴 High Priority** (Strongly recommended):
5. `Node.node_to_world` - World transform matrix
6. `Texture.has_file` - Texture type detection
7. `Texture.uv_set` - Multiple UV channels

**🟡 Medium Priority**:
8. Scene special collections (videos, shaders)
9. Mesh multi-material support
10. Node geometry transform

**🟢 Low Priority**:
11. NURBS objects (curves, surfaces, etc.)
12. Advanced features (cache, audio, LOD, etc.)

---

**Last Updated**: 2026-01-24
**Status**: Material system 100% complete, Scene core 53% complete
**Next Goal**: Implement Mesh tangent/bitangent for normal mapping support
