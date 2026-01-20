#!/usr/bin/env bash
set -eux

echo "=== ufbx-python Build Script ==="
echo ""

# Use PYTHON environment variable if set, otherwise try uv run python, then python3
if [ -n "$PYTHON" ]; then
    PYTHON_CMD="$PYTHON"
elif command -v uv &> /dev/null && uv run which python &> /dev/null; then
    PYTHON_CMD="uv run python"
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $PYTHON_CMD"

# 0. Display dependency version
echo "Current ufbx version:"
cat sfs-deps.json.lock
echo ""

# 1. Parse ufbx.h header file
echo "Step 1: Parsing ufbx.h..."
$PYTHON_CMD bindgen/ufbx_parser.py -i ufbx-c/ufbx.h -o bindgen/build/ufbx.json

# 2. Generate intermediate representation
echo "Step 2: Generating intermediate representation..."
$PYTHON_CMD bindgen/ufbx_ir.py

# 3. Generate Python binding code
echo "Step 3: Generating Python bindings..."
$PYTHON_CMD bindgen/generate_python.py

# 4. Compile C extension
echo "Step 4: Compiling C extension..."
$PYTHON_CMD setup.py build_ext --inplace

echo ""
echo "=== Build Complete! ==="
echo "ufbx version: $(grep ufbx= sfs-deps.json.lock)"
echo ""
echo "Next steps:"
echo "  - Run tests: python3 -m pytest tests/"
echo "  - Use Python REPL: python3 -c 'import ufbx; print(ufbx.__version__)'"
