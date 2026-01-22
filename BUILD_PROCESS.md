# Cython 构建流程详解

## 概览

从源码到可用 Python 模块的完整流程：

```
源文件                 Cython编译           C编译              链接              Python模块
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

_ufbx.pyx          →   _ufbx.c          →   _ufbx.o        →               →   _ufbx.so
                                            ufbx_wrapper.o                      (可被Python导入)
src/ufbx_wrapper.c →                   →   ufbx.o         →
../ufbx-c/ufbx.c   →                   →
```

## 详细步骤

### 步骤 1: Cython 转译 (.pyx → .c)

**输入**: `_ufbx.pyx` (Cython 源码)

**工具**: `cythonize()` 函数

**输出**: `_ufbx.c` (生成的 C 代码)

**过程**:
```python
# setup.py 中的配置
cythonize(
    extensions,
    compiler_directives={
        'language_level': 3,         # 使用 Python 3 语法
        'embedsignature': True,      # 在 docstring 中嵌入函数签名
    }
)
```

**生成的 C 代码包含**:
- Python C API 调用
- 类型转换代码
- 错误处理逻辑
- CPython 对象包装代码

例如，这段 Cython 代码：
```python
@property
def vertex_positions(self):
    cdef size_t count = 0
    cdef const float* data = ufbx_wrapper_mesh_get_vertex_positions(self._mesh, &count)
    # ...
```

会被转译成几百行 C 代码，包含：
- PyObject 创建和引用计数
- 类型检查和转换
- 异常处理


### 步骤 2: C 编译 (.c → .o)

**编译三个 C 文件**:

#### 2.1 编译 Cython 生成的代码
```bash
cc -c _ufbx.c -o _ufbx.o \
   -I. -Isrc -I.. \
   -I/path/to/numpy/include \
   -I/path/to/python/include \
   -O3
```

#### 2.2 编译 C wrapper
```bash
cc -c src/ufbx_wrapper.c -o ufbx_wrapper.o \
   -I. -Isrc -I.. \
   -O3
```

#### 2.3 编译 ufbx C 库
```bash
cc -c ../ufbx-c/ufbx.c -o ufbx.o \
   -I.. \
   -O3
```

**编译选项说明**:
- `-c`: 只编译不链接
- `-O3`: 最高级别优化
- `-I`: 指定头文件搜索路径
- `-fPIC`: 生成位置无关代码（用于共享库）


### 步骤 3: 链接 (.o → .so)

**将所有目标文件链接成共享库**:

```bash
cc -bundle -undefined dynamic_lookup \
   _ufbx.o \
   ufbx_wrapper.o \
   ufbx.o \
   -o _ufbx.cpython-312-darwin.so
```

**链接选项说明**:
- `-bundle`: 创建 macOS 动态库（Linux 上是 `-shared`）
- `-undefined dynamic_lookup`: 允许未定义符号（Python 运行时提供）
- 输出文件名格式: `_ufbx.cpython-{version}-{platform}.so`


### 步骤 4: Python 导入

**模块加载流程**:

```python
import ufbx
```

1. Python 查找 `ufbx/` 目录
2. 读取 `ufbx/__init__.py`
3. 执行 `from ._ufbx import ...`
4. 加载 `ufbx/_ufbx.cpython-312-darwin.so`
5. 初始化模块（调用 `PyInit__ufbx()`）
6. 导出 Scene, Node, Mesh, Material 等类


## 完整构建命令

### 开发环境构建（就地构建）

```bash
cd ufbx
python setup.py build_ext --inplace
```

**文件输出位置**:
```
ufbx/
├── _ufbx.c                          # Cython 生成
├── _ufbx.cpython-312-darwin.so      # 编译产物（就地）
└── build/
    ├── lib.macosx-11.0-arm64-cpython-312/
    │   └── _ufbx.cpython-312-darwin.so
    └── temp.macosx-11.0-arm64-cpython-312/
        ├── _ufbx.o
        ├── src/ufbx_wrapper.o
        └── ../ufbx-c/ufbx.o
```

### 安装构建

```bash
cd ufbx
python setup.py install
```

或使用 pip:
```bash
pip install .
```

**安装位置**:
```
site-packages/
├── ufbx/
│   ├── __init__.py
│   └── _ufbx.cpython-312-darwin.so
└── pyufbx-0.1.0.dist-info/
```


## 依赖关系图

```
_ufbx.pyx
├── imports numpy (编译时)
├── cimport numpy (Cython 静态类型)
├── includes "ufbx_wrapper.h"
└── calls ufbx_wrapper_* functions

ufbx_wrapper.c
├── includes "ufbx_wrapper.h"
├── includes "../ufbx-c/ufbx.h"
└── calls ufbx_* functions

ufbx.c
└── standalone C library
```


## 关键配置说明

### Extension 配置

```python
Extension(
    "_ufbx",                          # 模块名
    sources=[                         # 源文件列表
        "_ufbx.pyx",                  # Cython 源码
        "src/ufbx_wrapper.c",         # C wrapper
        "../ufbx-c/ufbx.c",           # ufbx C 库
    ],
    include_dirs=[                    # 头文件搜索路径
        ".",                          # 当前目录
        "src",                        # wrapper 头文件
        "..",                         # ufbx-c 头文件
        np.get_include(),             # numpy 头文件
    ],
    define_macros=[                   # 预处理宏定义
        ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")
    ],
    extra_compile_args=["-O3"],       # 额外编译参数
)
```


## 清理构建产物

```bash
# 清理所有生成文件
cd ufbx
rm -rf build/
rm -f _ufbx.c
rm -f _ufbx.*.so

# 或使用 setup.py
python setup.py clean --all
```


## 调试构建过程

### 查看详细编译信息

```bash
python setup.py build_ext --inplace --verbose
```

### 查看生成的 C 代码

Cython 会生成 `_ufbx.c`，可以查看具体的转译结果：

```bash
# 查看生成的 C 代码统计
wc -l _ufbx.c
# 约 78 万行（包含大量 Python C API 调用）

# 查看特定函数的转译
grep -A 20 "PyInit__ufbx" _ufbx.c
```


## 常见问题

### 1. 编译错误: numpy/arrayobject.h not found

**解决**:
```bash
pip install numpy
```

确保 `np.get_include()` 返回正确路径。


### 2. 运行时错误: undefined symbol

**原因**: 链接时缺少某些符号

**解决**: 检查 `sources` 列表是否包含所有需要的 C 文件


### 3. ImportError: cannot import name '_ufbx'

**原因**: .so 文件未生成或路径不对

**解决**:
```bash
# 确认 .so 文件存在
ls -la ufbx/*.so

# 使用 PYTHONPATH
PYTHONPATH=. python -c "import ufbx"
```


## 性能优化

### 编译优化

当前使用 `-O3` 最高优化级别。

可选优化选项：
```python
extra_compile_args=[
    "-O3",              # 最高优化
    "-march=native",    # 针对本机 CPU 优化
    "-flto",            # 链接时优化
]
```

### Cython 优化指令

```python
compiler_directives={
    'language_level': 3,
    'embedsignature': True,
    'boundscheck': False,      # 关闭边界检查（不安全）
    'wraparound': False,       # 关闭负索引（不安全）
    'cdivision': True,         # C 风格除法
    'initializedcheck': False, # 关闭初始化检查（不安全）
}
```

**注意**: 关闭安全检查会提升性能，但可能导致段错误。


## 与 CFFI 的对比

### CFFI 构建流程
```
Python FFI 描述 → CFFI 编译器 → C 代码 → 编译 → .so
                  (运行时调用)
```

### Cython 构建流程（当前）
```
.pyx → Cython 编译器 → C 代码 → 编译 → .so
       (编译时转译)
```

**优势**:
- Cython 在编译时完成类型转换，运行时开销更小
- 生成原生 C 代码，性能接近纯 C
- 更好的 numpy 集成（零拷贝数组视图）
