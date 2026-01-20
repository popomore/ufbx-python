"""
cffi 构建脚本 - 编译 ufbx C 扩展
"""
import os

from cffi import FFI

ffibuilder = FFI()

# 读取自动生成的 cdef 声明
cdef_file = os.path.join(os.path.dirname(__file__), '_ufbx_cdef.h')
with open(cdef_file) as f:
    cdef_content = f.read()

ffibuilder.cdef(cdef_content)

# 编译 C 源码
ffibuilder.set_source(
    "ufbx._ufbx",
    """
    #include "ufbx.h"
    """,
    sources=["ufbx-c/ufbx.c"],
    include_dirs=["ufbx-c"],
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
