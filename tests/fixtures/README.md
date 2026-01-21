# Test Fixtures

This directory contains test fixtures for ufbx-python tests.

## FBX Test Files

Test FBX files are not included in the repository due to their size. You can download test files from:

1. **ufbx test data repository**:
   ```bash
   curl -L -o tests/fixtures/maya_cube.fbx \
     "https://github.com/ufbx/ufbx/raw/master/test/data/maya_cube_6100_binary.fbx"
   ```

2. **Create your own test files** using any 3D modeling software (Blender, Maya, 3ds Max, etc.) that can export to FBX format.

## Running Tests with FBX Files

Once you have test FBX files in this directory, you can run:

```bash
# Run all tests
pytest tests/

# Run specific test with FBX loading
python tests/test_real_fbx.py
```

This will load and inspect the FBX file, demonstrating all the Python binding features.
