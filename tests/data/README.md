# Test Data

This directory contains test FBX files for running integration tests.

## Getting Test Files

Test FBX files are not included in the repository due to their size. You can download test files from:

1. **ufbx test data repository**:
   ```bash
   curl -L -o tests/data/maya_cube.fbx \
     "https://github.com/ufbx/ufbx/raw/master/test/data/maya_cube_6100_binary.fbx"
   ```

2. **Create your own test files** using any 3D modeling software (Blender, Maya, 3ds Max, etc.) that can export to FBX format.

## Running Tests with FBX Files

Once you have test FBX files in this directory, you can run:

```bash
python3 test_real_fbx.py
```

This will load and inspect the FBX file, demonstrating all the Python binding features.
