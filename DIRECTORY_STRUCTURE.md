# 目录结构说明

## 当前结构: Cython 实现（方案 B）

已完成目录重组，采用 Cython 实现替换原 CFFI 版本：

```
ufbx-python/
├── ufbx/                      # 原 CFFI 实现（保留作为备用）
│   ├── __init__.py
│   ├── core.py
│   ├── _ufbx.py
│   ├── _ufbx_build.py
│   ├── _ufbx_cdef.h
│   └── generated.py
│
├── ufbx_cy/                   # 新 Cython 实现（主要版本）
│   ├── __init__.py            # 导出 Scene, Node, Mesh 等
│   ├── src/                   # C wrapper 源码
│   │   ├── ufbx_wrapper.h
│   │   └── ufbx_wrapper.c
│   ├── _ufbx.pyx              # Cython 绑定
│   └── setup.py               # 独立构建配置
│
├── examples/
│   ├── basic_usage.py         # 基础使用示例
│   ├── test_cffi.py           # CFFI 版本测试
│   └── test_cython.py         # Cython 版本测试
│
├── bindgen/                   # CFFI 绑定生成器（保留）
│   └── generate_python.py
│
├── ufbx-c/                    # ufbx C 库（submodule）
│   ├── ufbx.h
│   └── ufbx.c
│
├── setup.py                   # 主构建配置
├── pyproject.toml
└── README.md
```

## 方案 B: 完全切换到 Cython（推荐用于生产）

```
ufbx-python/
├── src/                       # C wrapper 源码
│   ├── ufbx_wrapper.h
│   └── ufbx_wrapper.c
│
├── ufbx/                      # Python 包（Cython 实现）
│   ├── __init__.py            # 导出公共 API
│   └── _ufbx.pyx              # Cython 绑定实现
│
├── examples/
│   ├── basic_usage.py         # 基础示例
│   ├── load_mesh.py           # 加载网格示例
│   └── scene_hierarchy.py     # 场景层级示例
│
├── tests/                     # 单元测试
│   ├── test_scene.py
│   ├── test_mesh.py
│   └── test_node.py
│
├── docs/                      # 文档
│   ├── api.md
│   └── examples.md
│
├── ufbx-c/                    # ufbx C 库（submodule）
│   ├── ufbx.h
│   └── ufbx.c
│
├── setup.py                   # Cython 构建配置
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

## 构建和测试

### 构建

```bash
cd ufbx_cy
python setup.py build_ext --inplace
cd ..
```

### 测试

```bash
PYTHONPATH=. python examples/test_cython_basic.py <your_fbx_file>
```

## 方案 B: 完全切换到 Cython（可选）

如果将来决定完全移除 CFFI 版本，可以执行以下重组：

优点：
1. 保留 CFFI 版本作为参考和备用
2. 逐步迁移到 Cython
3. 可以对比两个实现
4. 用户可以选择使用哪个版本

使用：
```python
# CFFI 版本
import ufbx
scene = ufbx.load_file("model.fbx")

# Cython 版本（推荐）
import ufbx_cy
with ufbx_cy.load_file("model.fbx") as scene:
    ...
```
