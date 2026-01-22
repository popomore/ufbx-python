"""测试 Cython 版本的 ufbx 绑定"""
import sys
import ufbx

fbx_path = sys.argv[1] if len(sys.argv) > 1 else "test.fbx"
print(f"加载文件: {fbx_path}\n")

# 使用 with 语句自动管理生命周期
with ufbx.load_file(fbx_path) as scene:
    print("✓ 场景加载成功\n")

    # 测试节点
    print(f"=== 节点信息 ===")
    nodes = scene.nodes
    print(f"总节点数: {len(nodes)}")
    for i, node in enumerate(nodes[:5]):  # 只显示前 5 个
        print(f"  节点 {i}: {node.name}")
        if node.mesh:
            print(f"    -> 有 mesh")

    # 测试网格
    print(f"\n=== 网格信息 ===")
    meshes = scene.meshes
    print(f"总网格数: {len(meshes)}")

    for i, mesh in enumerate(meshes):
        print(f"\n网格 {i}: {mesh.name}")
        print(f"  顶点数: {mesh.num_vertices}")
        print(f"  索引数: {mesh.num_indices}")
        print(f"  面数: {mesh.num_faces}")
        print(f"  三角形数: {mesh.num_triangles}")

        # 测试访问顶点数据
        positions = mesh.vertex_positions
        if positions is not None:
            print(f"  顶点位置: shape={positions.shape}, dtype={positions.dtype}")
            if len(positions) > 0:
                print(f"  第一个顶点: {positions[0]}")

        normals = mesh.vertex_normals
        if normals is not None:
            print(f"  顶点法线: shape={normals.shape}")

        uvs = mesh.vertex_uvs
        if uvs is not None:
            print(f"  顶点 UV: shape={uvs.shape}")

        indices = mesh.indices
        if indices is not None:
            print(f"  索引: shape={indices.shape}, dtype={indices.dtype}")

        # 材质
        materials = mesh.materials
        if materials:
            print(f"  材质数: {len(materials)}")
            for j, mat in enumerate(materials[:3]):
                print(f"    材质 {j}: {mat.name}")

    # 测试材质
    print(f"\n=== 材质信息 ===")
    materials = scene.materials
    print(f"总材质数: {len(materials)}")
    for i, material in enumerate(materials[:5]):
        print(f"  材质 {i}: {material.name}")

    # 测试根节点
    print(f"\n=== 根节点 ===")
    root = scene.root_node
    if root:
        print(f"根节点: {root.name}")
        print(f"子节点数: {len(root.children)}")
        print(f"是根节点: {root.is_root}")

        # 测试变换矩阵
        world_transform = root.world_transform
        print(f"世界变换矩阵 shape: {world_transform.shape}")

print("\n✓ 所有测试完成")
