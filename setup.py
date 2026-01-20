"""
ufbx-python setup script
"""

import os

from setuptools import find_packages, setup


# 读取版本号
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "ufbx", "__init__.py")
    with open(version_file) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip("'\"")
    return "0.1.0"


# 读取长描述
def get_long_description():
    readme_file = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_file):
        with open(readme_file, encoding="utf-8") as f:
            return f.read()
    return ""


setup(
    name="pyufbx",
    version=get_version(),
    description="Python bindings for ufbx - Single source file FBX loader",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="ufbx-python contributors",
    url="https://github.com/popomore/ufbx-python",
    project_urls={
        "Bug Reports": "https://github.com/popomore/ufbx-python/issues",
        "Source": "https://github.com/popomore/ufbx-python",
        "Documentation": "https://github.com/popomore/ufbx-python#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "bindgen"]),
    package_data={
        "ufbx": ["*.h"],  # 包含生成的头文件
    },
    setup_requires=["cffi>=1.15.0"],
    install_requires=[
        "cffi>=1.15.0",
    ],
    cffi_modules=["ufbx/_ufbx_build.py:ffibuilder"],
    python_requires=">=3.9",
    keywords="fbx 3d graphics modeling autodesk loader",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
