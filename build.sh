#!/usr/bin/env bash
set -eux

echo "=== ufbx-python Build Script ==="
echo ""

# 0. Display dependency version
echo "Current ufbx version:"
cat sfs-deps.json.lock
echo ""

# 1. Parse ufbx.h header file
echo "Step 1: Parsing ufbx.h..."
python3 bindgen/ufbx_parser.py -i ufbx-c/ufbx.h -o bindgen/build/ufbx.json

# 2. Generate intermediate representation
echo "Step 2: Generating intermediate representation..."
python3 bindgen/ufbx_ir.py

# 3. Generate Python binding code
echo "Step 3: Generating Python bindings..."
python3 bindgen/generate_python.py

# 4. Compile C extension
echo "Step 4: Compiling C extension..."
python3 setup.py build_ext --inplace

echo ""
echo "=== Build Complete! ==="
echo "ufbx version: $(grep ufbx= sfs-deps.json.lock)"
echo ""
echo "Next steps:"
echo "  - Run tests: python3 -m pytest tests/"
echo "  - Use Python REPL: python3 -c 'import ufbx; print(ufbx.__version__)'"
