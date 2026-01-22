"""
Setup script for ufbx Python bindings using Cython
"""
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import os

# Define the extension
extensions = [
    Extension(
        "_ufbx",
        sources=[
            "_ufbx.pyx",
            "src/ufbx_wrapper.c",
            "../ufbx-c/ufbx.c",
        ],
        include_dirs=[
            ".",
            "src",
            "..",
            np.get_include(),
        ],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        extra_compile_args=["-O3"],
    )
]

setup(
    name="pyufbx",
    version="0.1.0",
    packages=["ufbx"],
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': 3,
            'embedsignature': True,
        }
    ),
    install_requires=["numpy"],
    zip_safe=False,
)
