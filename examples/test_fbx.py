"""
使用 pyufbx 读取 FBX 文件的测试脚本
"""

import os
import sys

import ufbx


def read_fbx_file(fbx_path: str):
    """
    使用 pyufbx 读取 FBX 文件

    Args:
        fbx_path: FBX 文件路径
    """
    if not os.path.exists(fbx_path):
        print(f"错误: 文件不存在: {fbx_path}")
        return None

    print(f"正在读取 FBX 文件: {fbx_path}")

    try:
        # 使用上下文管理器加载 FBX 场景（推荐方式）
        with ufbx.load_file(fbx_path) as scene:
            print("✓ 成功加载 FBX 文件")
            print(f"场景统计: {scene}")
            print()

            # 遍历所有节点 - 从根节点递归遍历
            print("=== 节点信息 ===")
            node_count = 0
            mesh_count = 0

            def traverse_node(node, depth=0, is_root_node=False):
                """递归遍历节点"""
                nonlocal node_count, mesh_count
                # 跳过根节点
                if not is_root_node:
                    node_count += 1
                    node_name = node.name
                    indent = "  " * depth
                    print(f"{indent}节点 {node_count}: {node_name}")

                    # 检查是否有网格数据
                    if node.mesh:
                        mesh_count += 1
                        mesh = node.mesh
                        try:
                            mesh_name = mesh.name
                        except Exception as e:
                            mesh_name = f"[无法获取名称: {e}]"
                        print(f"{indent}  [Mesh: {mesh_name}]")

                        # 获取顶点数
                        print(f"{indent}    顶点数: {mesh.num_vertices}")
                        print(f"{indent}    索引数: {mesh.num_indices}")

                        # 获取面数
                        print(f"{indent}    面数: {mesh.num_faces}")
                        print(f"{indent}    三角形数: {mesh.num_triangles}")

                        # 获取顶点位置（前几个）
                        if mesh.num_vertices > 0:
                            positions = mesh.vertex_position
                            sample_count = min(3, len(positions))
                            if sample_count > 0:
                                print(f"{indent}    顶点位置示例 (前 {sample_count} 个):")
                                for i in range(sample_count):
                                    pos = positions[i]
                                    print(f"{indent}      [{i}]: ({pos.x:.3f}, {pos.y:.3f}, {pos.z:.3f})")

                    # 检查是否有骨骼
                    if node.bone:
                        bone = node.bone
                        print(f"{indent}  [Bone: {bone.name}]")
                        print(f"{indent}    半径: {bone.radius:.3f}")
                        print(f"{indent}    相对长度: {bone.relative_length:.3f}")

                    # 检查是否有灯光
                    if node.light:
                        light = node.light
                        print(f"{indent}  [Light: {light.name}]")
                        color = light.color
                        print(f"{indent}    颜色: ({color.x:.3f}, {color.y:.3f}, {color.z:.3f})")
                        print(f"{indent}    强度: {light.intensity:.3f}")

                    # 检查是否有相机
                    if node.camera:
                        camera = node.camera
                        print(f"{indent}  [Camera: {camera.name}]")
                        print(f"{indent}    近平面: {camera.near_plane:.3f}")
                        print(f"{indent}    远平面: {camera.far_plane:.3f}")

                # 递归遍历子节点
                for child in node.children:
                    traverse_node(child, depth + 1)

            # 直接遍历所有节点（避免访问 root_node.children 可能导致的段错误）
            print("注意: 直接遍历所有节点（跳过层次结构）")
            for node in scene.nodes:
                try:
                    node_count += 1
                    node_name = node.name
                    print(f"节点 {node_count}: {node_name}")
                    
                    # 检查是否有网格数据
                    if node.mesh:
                        mesh_count += 1
                        mesh = node.mesh
                        try:
                            mesh_name = mesh.name
                        except Exception as e:
                            mesh_name = f"[无法获取名称: {e}]"
                        print(f"  [Mesh: {mesh_name}]")
                        
                        # 获取顶点数
                        try:
                            print(f"    顶点数: {mesh.num_vertices}")
                            print(f"    索引数: {mesh.num_indices}")
                            print(f"    面数: {mesh.num_faces}")
                            print(f"    三角形数: {mesh.num_triangles}")
                        except Exception as e:
                            print(f"    警告: 无法获取网格统计信息: {e}")
                            
                except Exception as e:
                    print(f"节点 {node_count}: [错误: {e}]")

            print(f"\n总节点数: {node_count}")
            print(f"包含网格的节点数: {mesh_count}")

            # 获取场景中的网格信息
            print("\n=== 场景网格信息 ===")
            meshes = scene.meshes
            if meshes:
                print(f"场景总网格数: {len(meshes)}")
                for i, mesh in enumerate(meshes):
                    print(f"\n网格 {i + 1}: {mesh.name}")
                    print(f"  顶点数: {mesh.num_vertices}")
                    print(f"  索引数: {mesh.num_indices}")
                    print(f"  面数: {mesh.num_faces}")
                    print(f"  三角形数: {mesh.num_triangles}")

                    # 材质信息
                    materials = mesh.materials
                    if materials:
                        print(f"  材质数: {len(materials)}")
                        for j, mat in enumerate(materials):
                            print(f"    材质 {j + 1}: {mat.name}")

            # 获取材质信息
            print("\n=== 材质信息 ===")
            materials = scene.materials
            if materials:
                print(f"总材质数: {len(materials)}")
                for i, material in enumerate(materials):
                    print(f"  材质 {i + 1}: {material.name}")
                    # 获取材质的纹理
                    textures = material.textures
                    if textures:
                        print(f"    纹理数: {len(textures)}")
                        for j, tex in enumerate(textures):
                            print(f"      纹理 {j + 1}: {tex.name}")

            # 获取纹理信息
            print("\n=== 纹理信息 ===")
            textures = scene.textures
            if textures:
                print(f"总纹理数: {len(textures)}")
                for i, texture in enumerate(textures):
                    print(f"  纹理 {i + 1}: {texture.name}")
                    if texture.filename:
                        print(f"    文件名: {texture.filename}")
                    if texture.absolute_filename:
                        print(f"    绝对路径: {texture.absolute_filename}")
                    if texture.relative_filename:
                        print(f"    相对路径: {texture.relative_filename}")

            # 获取骨骼信息（通过节点）
            print("\n=== 骨骼信息 ===")
            bone_count = 0
            for node in scene.nodes:
                if node.bone:
                    bone_count += 1
                    bone = node.bone
                    print(f"  骨骼 {bone_count}: {bone.name} (节点: {node.name})")
                    print(f"    半径: {bone.radius:.3f}")
                    print(f"    相对长度: {bone.relative_length:.3f}")
            if bone_count == 0:
                print("  未找到骨骼")

            # 获取灯光信息
            print("\n=== 灯光信息 ===")
            lights = scene.lights
            if lights:
                print(f"总灯光数: {len(lights)}")
                for i, light in enumerate(lights):
                    color = light.color
                    print(f"  灯光 {i + 1}: {light.name}")
                    print(f"    颜色: ({color.x:.3f}, {color.y:.3f}, {color.z:.3f})")
                    print(f"    强度: {light.intensity:.3f}")

            # 获取相机信息
            print("\n=== 相机信息 ===")
            cameras = scene.cameras
            if cameras:
                print(f"总相机数: {len(cameras)}")
                for i, camera in enumerate(cameras):
                    print(f"  相机 {i + 1}: {camera.name}")
                    print(f"    近平面: {camera.near_plane:.3f}")
                    print(f"    远平面: {camera.far_plane:.3f}")
                    resolution = camera.resolution
                    print(f"    分辨率: {resolution.x:.0f} x {resolution.y:.0f}")

            # 获取动画信息
            print("\n=== 动画信息 ===")
            anim_stacks = scene.anim_stacks
            if anim_stacks:
                print(f"动画堆栈数: {len(anim_stacks)}")
                for i, anim_stack in enumerate(anim_stacks):
                    print(f"  动画堆栈 {i + 1}: {anim_stack.name}")
                    print(f"    开始时间: {anim_stack.time_begin:.3f}")
                    print(f"    结束时间: {anim_stack.time_end:.3f}")
            else:
                print("  未找到动画")

            print("\n✓ FBX 文件读取成功")
            return scene

    except ufbx.UfbxFileNotFoundError as e:
        print(f"错误: 文件未找到 - {e}")
        return None
    except ufbx.UfbxError as e:
        print(f"错误: 读取 FBX 文件时出错 - {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    # 测试示例
    if len(sys.argv) > 1:
        fbx_file = sys.argv[1]
    else:
        # 默认测试路径（需要根据实际情况修改）
        fbx_file = "test.fbx"
        print(f"未指定文件路径，使用默认路径: {fbx_file}")
        print("用法: python test_fbx.py <fbx_file_path>")
        print()

    scene = read_fbx_file(fbx_file)

    if scene:
        print("\n✓ 测试完成")
    else:
        print("\n✗ 测试失败")
