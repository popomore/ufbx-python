#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates how to use ufbx-python to load and explore FBX files
"""

import sys

import ufbx


def get_scene_statistics(scene):
    """Collect detailed scene statistics"""
    stats = {
        "nodes": len(scene.nodes),
        "nodes_with_mesh": 0,
        "leaf_nodes": 0,
        "meshes": len(scene.meshes),
        "total_vertices": 0,
        "total_triangles": 0,
        "total_faces": 0,
        "materials": len(scene.materials),
    }

    # Analyze nodes
    for node in scene.nodes:
        if node.mesh:
            stats["nodes_with_mesh"] += 1
        if len(node.children) == 0:
            stats["leaf_nodes"] += 1

    # Analyze meshes
    for mesh in scene.meshes:
        stats["total_vertices"] += mesh.num_vertices
        stats["total_triangles"] += mesh.num_triangles
        stats["total_faces"] += mesh.num_faces

    return stats


def get_coordinate_system_info(axes):
    """Analyze coordinate system and return description"""
    # Coordinate axis direction mapping
    axis_names = {0: "+X", 1: "-X", 2: "+Y", 3: "-Y", 4: "+Z", 5: "-Z", 6: "Unknown"}

    right_name = axis_names.get(axes.right.value, "Unknown")
    up_name = axis_names.get(axes.up.value, "Unknown")
    front_name = axis_names.get(axes.front.value, "Unknown")

    # Construct coordinate system transformation matrix (column-major)
    # This matrix represents the scene coordinate axes in the standard coordinate system
    matrix = [[0.0, 0.0, 0.0, 0.0] for _ in range(4)]

    if axes.right.value < 6 and axes.up.value < 6 and axes.front.value < 6:
        # Extract direction and axis
        right_axis = axes.right.value // 2  # 0=X, 1=Y, 2=Z
        right_sign = 1.0 if axes.right.value % 2 == 0 else -1.0
        up_axis = axes.up.value // 2
        up_sign = 1.0 if axes.up.value % 2 == 0 else -1.0
        front_axis = axes.front.value // 2
        front_sign = 1.0 if axes.front.value % 2 == 0 else -1.0

        # Column-major matrix: matrix[col][row]
        # Column 0: Right
        matrix[right_axis][0] = right_sign
        # Column 1: Up
        matrix[up_axis][1] = up_sign
        # Column 2: Front
        matrix[front_axis][2] = front_sign
        # Column 3: Translation / W
        matrix[3][3] = 1.0

        # Determine handedness (right-handed or left-handed coordinate system)
        right_vec = [0, 0, 0]
        up_vec = [0, 0, 0]
        right_vec[right_axis] = right_sign
        up_vec[up_axis] = up_sign

        # Calculate cross product (right × up)
        cross = [0, 0, 0]
        cross[0] = right_vec[1] * up_vec[2] - right_vec[2] * up_vec[1]
        cross[1] = right_vec[2] * up_vec[0] - right_vec[0] * up_vec[2]
        cross[2] = right_vec[0] * up_vec[1] - right_vec[1] * up_vec[0]

        # Check if cross product matches front direction
        front_vec = [0, 0, 0]
        front_vec[front_axis] = front_sign

        # Determine handedness using dot product (more robust than exact match)
        dot = cross[0] * front_vec[0] + cross[1] * front_vec[1] + cross[2] * front_vec[2]

        if dot > 0.5:
            handedness = "Right-handed"
        elif dot < -0.5:
            handedness = "Left-handed"
        else:
            handedness = "Unknown"
    else:
        handedness = "Unknown"
        # Identity matrix
        for i in range(4):
            matrix[i][i] = 1.0

    # Common coordinate system descriptions
    system_desc = ""
    if up_name == "+Y" and front_name == "+Z":
        system_desc = "Y-up, Z-forward (OpenGL/Blender style)"
    elif up_name == "+Y" and front_name == "-Z":
        system_desc = "Y-up, -Z-forward (Unity style)"
    elif up_name == "+Z" and front_name == "+Y":
        system_desc = "Z-up, Y-forward (3ds Max style)"
    elif up_name == "+Z" and front_name == "-Y":
        system_desc = "Z-up, -Y-forward (Maya style)"

    return {
        "right": right_name,
        "up": up_name,
        "front": front_name,
        "handedness": handedness,
        "description": system_desc,
        "matrix": matrix,
    }


def print_node_hierarchy(node, depth=0, max_depth=3):
    """Recursively print node hierarchy structure"""
    if depth > max_depth:
        return

    indent = "  " * depth
    mesh_info = " [mesh]" if node.mesh else ""
    structure_note = ""
    if node.mesh and node.children:
        structure_note = " (note: mesh node has children)"

    print(f"{indent}- {node.name}{mesh_info}{structure_note}")

    # Show node's parent
    if depth == 0 and node.parent:
        print(f"{indent}  (parent: {node.parent.name})")

    # Recursively show child nodes
    for child in node.children:
        print_node_hierarchy(child, depth + 1, max_depth)


def extract_euler_angles(matrix, scale_x, scale_y, scale_z):
    """Extract Euler angles from rotation matrix (XYZ order, in degrees)"""
    import math

    # Normalize rotation matrix (remove scaling)
    # Matrix is column-major: columns are basis vectors
    if scale_x == 0 or scale_y == 0 or scale_z == 0:
        return (0.0, 0.0, 0.0)

    # Extract column vectors and normalize
    r00 = matrix[0, 0] / scale_x
    r10 = matrix[1, 0] / scale_x
    r20 = matrix[2, 0] / scale_x
    matrix[0, 1] / scale_y
    r11 = matrix[1, 1] / scale_y
    r21 = matrix[2, 1] / scale_y
    matrix[0, 2] / scale_z
    r12 = matrix[1, 2] / scale_z
    r22 = matrix[2, 2] / scale_z

    # Extract Euler angles (XYZ order)
    # Note: Using standard XYZ rotation order
    if abs(r20) < 0.99999:
        rot_y = math.asin(-r20)
        rot_x = math.atan2(r21, r22)
        rot_z = math.atan2(r10, r00)
    else:
        # Gimbal lock case
        rot_y = -math.pi / 2 if r20 > 0 else math.pi / 2
        rot_x = math.atan2(-r12, r11)
        rot_z = 0

    # Convert to degrees
    return (math.degrees(rot_x), math.degrees(rot_y), math.degrees(rot_z))


def print_transform_info(node):
    """Print node transformation information"""
    import math

    # Local transform (relative to parent) - returns 4x4 numpy array (column-major)
    # Column-major means: columns are basis vectors [right, up, forward, position]
    local_matrix = node.local_transform
    print("      - Transform (Local, relative to parent):")

    # Extract position (4th column: column 3)
    pos_x, pos_y, pos_z = local_matrix[0, 3], local_matrix[1, 3], local_matrix[2, 3]
    print(f"          Position: ({pos_x:8.3f}, {pos_y:8.3f}, {pos_z:8.3f})")

    # Extract scale (length of each column vector)
    # Column 0: X-axis basis vector
    scale_x = math.sqrt(local_matrix[0, 0] ** 2 + local_matrix[1, 0] ** 2 + local_matrix[2, 0] ** 2)
    # Column 1: Y-axis basis vector
    scale_y = math.sqrt(local_matrix[0, 1] ** 2 + local_matrix[1, 1] ** 2 + local_matrix[2, 1] ** 2)
    # Column 2: Z-axis basis vector
    scale_z = math.sqrt(local_matrix[0, 2] ** 2 + local_matrix[1, 2] ** 2 + local_matrix[2, 2] ** 2)

    scale_note = "uniform" if abs(scale_x - scale_y) < 0.001 and abs(scale_y - scale_z) < 0.001 else "non-uniform"

    print(f"          Scale:    ({scale_x:8.3f}, {scale_y:8.3f}, {scale_z:8.3f}) [{scale_note}]")

    # Extract rotation (Euler angles)
    rot_x, rot_y, rot_z = extract_euler_angles(local_matrix, scale_x, scale_y, scale_z)
    print(f"          Rotation: ({rot_x:8.3f}°, {rot_y:8.3f}°, {rot_z:8.3f}°) [derived Euler, from baked matrix, XYZ]")

    # Check if there are significant transformations
    has_translation = abs(pos_x) > 0.001 or abs(pos_y) > 0.001 or abs(pos_z) > 0.001
    has_rotation = abs(rot_x) > 0.01 or abs(rot_y) > 0.01 or abs(rot_z) > 0.01
    has_scale = abs(scale_x - 1.0) > 0.001 or abs(scale_y - 1.0) > 0.001 or abs(scale_z - 1.0) > 0.001

    transform_type = []
    if has_translation:
        transform_type.append("Translation")
    if has_rotation:
        transform_type.append("Rotation")
    if has_scale:
        transform_type.append("Scale")

    if transform_type:
        print(f"          Has: {', '.join(transform_type)}")
    else:
        print("          Has: Identity (no transform)")

    # World transform
    world_matrix = node.world_transform
    print("      - Transform (World, inherited through hierarchy):")
    world_pos_x = world_matrix[0, 3]
    world_pos_y = world_matrix[1, 3]
    world_pos_z = world_matrix[2, 3]
    print(f"          Position: ({world_pos_x:8.3f}, {world_pos_y:8.3f}, {world_pos_z:8.3f})")

    # World space scale and rotation
    world_scale_x = math.sqrt(world_matrix[0, 0] ** 2 + world_matrix[1, 0] ** 2 + world_matrix[2, 0] ** 2)
    world_scale_y = math.sqrt(world_matrix[0, 1] ** 2 + world_matrix[1, 1] ** 2 + world_matrix[2, 1] ** 2)
    world_scale_z = math.sqrt(world_matrix[0, 2] ** 2 + world_matrix[1, 2] ** 2 + world_matrix[2, 2] ** 2)
    world_rot_x, world_rot_y, world_rot_z = extract_euler_angles(world_matrix, world_scale_x, world_scale_y, world_scale_z)
    print(f"          Rotation: ({world_rot_x:8.3f}°, {world_rot_y:8.3f}°, {world_rot_z:8.3f}°) [XYZ Euler]")


def format_texture_info(texture, indent="              "):
    """Format detailed texture information"""
    if not texture:
        return None

    info = []
    if texture.name:
        info.append(f"{indent}Name: {texture.name}")
    if texture.filename:
        info.append(f"{indent}File: {texture.filename}")
    if texture.relative_filename:
        info.append(f"{indent}Relative: {texture.relative_filename}")
    if texture.absolute_filename:
        info.append(f"{indent}Absolute: {texture.absolute_filename}")
    info.append(f"{indent}Type: {texture.type}")

    return "\n".join(info) if info else None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 basic_usage.py <fbx_file_path>")
        print("\nExample:")
        print("  python3 basic_usage.py model.fbx")
        sys.exit(1)

    filename = sys.argv[1]

    print("=== ufbx-python Basic Usage Example ===")
    print(f"Version: {ufbx.__version__}")
    print()

    try:
        # Load scene using context manager
        with ufbx.load_file(filename) as scene:
            print(f"✓ Successfully loaded: {filename}")
            print()

            # Scene statistics
            stats = get_scene_statistics(scene)
            print("📊 Scene Statistics:")
            print(f"  Nodes: {stats['nodes']}")
            print(f"    - With mesh: {stats['nodes_with_mesh']}")
            print(f"    - Leaf nodes: {stats['leaf_nodes']}")
            mesh_note = ""
            if stats["meshes"] == 1 and stats["nodes"] > 1:
                mesh_note = " (note: many nodes reference a single mesh)"
            print(f"  Meshes: {stats['meshes']}{mesh_note}")
            if stats["meshes"] > 0:
                print(f"    - Total vertices: {stats['total_vertices']:,}")
                print(f"    - Total faces: {stats['total_faces']:,}")
                print(f"    - Total triangles: {stats['total_triangles']:,}")
            print(f"  Materials: {stats['materials']}")
            print()

            # Coordinate system
            axes = scene.axes
            coord_info = get_coordinate_system_info(axes)
            print("🧭 Coordinate System:")
            print("  Axes mapping:")
            print(f"    - Right:  {coord_info['right']}")
            print(f"    - Up:     {coord_info['up']}")
            print(f"    - Front:  {coord_info['front']}")
            print("  System type:")
            print(f"    - Handedness: {coord_info['handedness']}")
            if coord_info["description"]:
                print(f"    - Description: {coord_info['description']} (axis conversion likely applied)")
            print("  Basis matrix (4x4, column-major):")
            matrix = coord_info["matrix"]
            for row in range(4):
                print(f"    [{matrix[0][row]:6.1f} {matrix[1][row]:6.1f} {matrix[2][row]:6.1f} {matrix[3][row]:6.1f}]")
            print()

            # Root node and hierarchy
            root = scene.root_node
            if root:
                print(f"🌳 Scene Hierarchy (root: '{root.name}', {len(root.children)} children):")
                print_node_hierarchy(root, max_depth=10)
                print()

            # All nodes details
            if scene.nodes:
                print(f"🎯 Node Details ({len(scene.nodes)} nodes):")
                for idx, node in enumerate(scene.nodes):
                    print(f"\n  [{idx}] Node: '{node.name}'")
                    print(f"      - Has mesh: {node.mesh is not None}")
                    if node.mesh:
                        print(f"        Mesh: '{node.mesh.name}' ({node.mesh.num_vertices} vertices)")
                    print(f"      - Children: {len(node.children)}")
                    if node.children:
                        child_names = [f"'{c.name}'" for c in node.children[:3]]
                        if len(node.children) > 3:
                            child_names.append(f"... +{len(node.children) - 3} more")
                        print(f"        {', '.join(child_names)}")
                    print(f"      - Parent: {node.parent.name if node.parent else 'None'}")
                    print_transform_info(node)
                print()

            # Mesh details
            if scene.meshes:
                print(f"📐 Mesh Details ({len(scene.meshes)} meshes):")
                for i, mesh in enumerate(scene.meshes):
                    print(f"\n  [{i}] Mesh: '{mesh.name}'")
                    print(f"      - Vertices: {mesh.num_vertices:,}")
                    print(f"      - Indices: {mesh.num_indices:,}")
                    print(f"      - Faces: {mesh.num_faces:,}")
                    print(f"      - Triangles: {mesh.num_triangles:,}")

                    # Vertex attributes
                    positions = mesh.vertex_positions
                    normals = mesh.vertex_normals
                    uvs = mesh.vertex_uvs

                    print("      - Vertex attributes:")
                    if positions is not None:
                        print(f"        ✓ Positions: shape={positions.shape}, dtype={positions.dtype}")
                        if len(positions) > 0:
                            print(
                                f"          First vertex: ({positions[0][0]:.3f}, {positions[0][1]:.3f}, {positions[0][2]:.3f})"
                            )

                    if normals is not None:
                        note = ""
                        if positions is not None and len(normals) != len(positions):
                            note = " (note: normal count != vertex count)"

                        print(f"        ✓ Normals: shape={normals.shape}{note}")
                        if len(normals) > 0:
                            print(f"          First normal: ({normals[0][0]:.3f}, {normals[0][1]:.3f}, {normals[0][2]:.3f})")

                    if uvs is not None:
                        print(f"        ✓ UVs: shape={uvs.shape}")
                        if len(uvs) > 0:
                            print(f"          First UV: ({uvs[0][0]:.3f}, {uvs[0][1]:.3f})")

                    # Indices
                    indices = mesh.indices
                    if indices is not None and len(indices) > 0:
                        print(f"        ✓ Indices: shape={indices.shape}")
                        print(f"          First triangle: [{indices[0]}, {indices[1]}, {indices[2]}]")

                print()

            # Material information
            if scene.materials:
                print(f"🎨 Material Details ({len(scene.materials)} materials):")

                # Collect statistics
                shader_types = {}
                shading_models = {}
                materials_with_textures = 0

                for material in scene.materials:
                    # Count shader types
                    shader_type = material.shader_type
                    shader_types[shader_type] = shader_types.get(shader_type, 0) + 1

                    # Count shading models
                    shading_model = material.shading_model_name
                    if shading_model:
                        shading_models[shading_model] = shading_models.get(shading_model, 0) + 1

                    # Count materials with textures (check common maps)
                    has_texture = any(
                        [
                            material.pbr_base_color.texture_enabled and material.pbr_base_color.texture,
                            material.pbr_normal_map.texture_enabled and material.pbr_normal_map.texture,
                            material.fbx_diffuse_color.texture_enabled and material.fbx_diffuse_color.texture,
                        ]
                    )
                    if has_texture:
                        materials_with_textures += 1

                # Display statistics
                print("  Overview:")
                print(f"    - Materials with textures: {materials_with_textures}")
                if shading_models:
                    print(f"    - Shading models: {', '.join(f'{k} ({v})' for k, v in sorted(shading_models.items()))}")
                print()

                # Display individual materials
                print("  Materials:")
                for i, material in enumerate(scene.materials):
                    print(f"\n    [{i}] '{material.name}'")

                    # Shading information
                    shading_info = []
                    if material.shading_model_name:
                        shading_info.append(f"model={material.shading_model_name}")
                    shading_info.append(f"shader_type={material.shader_type}")
                    print(f"        - Shading: {', '.join(shading_info)}")

                    # PBR properties
                    print("        - PBR properties:")

                    # Base properties
                    base_color = material.pbr_base_color
                    if base_color.has_value:
                        r, g, b, a = base_color.value_vec4
                        print(f"            Base color: RGB({r:.3f}, {g:.3f}, {b:.3f}), A={a:.3f}")
                    if base_color.texture_enabled and base_color.texture:
                        print("            Base color texture:")
                        tex_info = format_texture_info(base_color.texture)
                        if tex_info:
                            print(tex_info)

                    roughness = material.pbr_roughness
                    if roughness.has_value:
                        print(f"            Roughness: {roughness.value_vec4[0]:.3f}")
                    if roughness.texture_enabled and roughness.texture:
                        print("            Roughness texture:")
                        tex_info = format_texture_info(roughness.texture)
                        if tex_info:
                            print(tex_info)

                    metalness = material.pbr_metalness
                    if metalness.has_value:
                        print(f"            Metalness: {metalness.value_vec4[0]:.3f}")
                    if metalness.texture_enabled and metalness.texture:
                        print("            Metalness texture:")
                        tex_info = format_texture_info(metalness.texture)
                        if tex_info:
                            print(tex_info)

                    # Extended properties
                    emission = material.pbr_emission_color
                    if emission.has_value:
                        r, g, b, a = emission.value_vec4
                        print(f"            Emission: RGB({r:.3f}, {g:.3f}, {b:.3f})")
                    if emission.texture_enabled and emission.texture:
                        print("            Emission texture:")
                        tex_info = format_texture_info(emission.texture)
                        if tex_info:
                            print(tex_info)

                    opacity = material.pbr_opacity
                    if opacity.has_value:
                        alpha = opacity.value_vec4[0]
                        print(f"            Opacity: {alpha:.3f}")
                    if opacity.texture_enabled and opacity.texture:
                        print("            Opacity texture:")
                        tex_info = format_texture_info(opacity.texture)
                        if tex_info:
                            print(tex_info)

                    # Maps
                    normal_map = material.pbr_normal_map
                    if normal_map.texture_enabled and normal_map.texture:
                        print("            Normal map:")
                        tex_info = format_texture_info(normal_map.texture)
                        if tex_info:
                            print(tex_info)

                    ao_map = material.pbr_ambient_occlusion
                    if ao_map.texture_enabled and ao_map.texture:
                        print("            AO map:")
                        tex_info = format_texture_info(ao_map.texture)
                        if tex_info:
                            print(tex_info)

                    # FBX properties (for compatibility)
                    fbx_diffuse = material.fbx_diffuse_color
                    if fbx_diffuse.texture_enabled or (
                        fbx_diffuse.has_value and any(v != 0 for v in fbx_diffuse.value_vec4[:3])
                    ):
                        print("        - FBX properties:")
                        if fbx_diffuse.has_value:
                            r, g, b, a = fbx_diffuse.value_vec4
                            print(f"            Diffuse color: RGB({r:.3f}, {g:.3f}, {b:.3f})")
                        if fbx_diffuse.texture_enabled and fbx_diffuse.texture:
                            print("            Diffuse texture:")
                            tex_info = format_texture_info(fbx_diffuse.texture)
                            if tex_info:
                                print(tex_info)

                print()

            # Texture information
            if scene.textures:
                print(f"🖼️  Texture Details ({len(scene.textures)} textures):")
                print()

                for i, texture in enumerate(scene.textures):
                    print(f"  [{i}] Texture: '{texture.name}'")

                    # File information
                    if texture.filename:
                        print(f"      - Filename: {texture.filename}")
                    if texture.relative_filename:
                        print(f"      - Relative: {texture.relative_filename}")
                    if texture.absolute_filename:
                        print(f"      - Absolute: {texture.absolute_filename}")

                    # Texture type
                    print(f"      - Type: {texture.type}")

                    print()

    except FileNotFoundError:
        print(f"❌ Error: File not found - {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: Load failed - {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
