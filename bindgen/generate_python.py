#!/usr/bin/env python3
"""
Python binding generator for ufbx

Based on the implementation of generate_rust.py, generates Python (cffi) bindings for ufbx
"""

import json
import os
import sys
from typing import Dict, List, Set

class PythonGenerator:
    def __init__(self, ir_path: str):
        with open(ir_path, 'r') as f:
            self.ir = json.load(f)

        self.structs = self.ir.get('structs', {})
        self.enums = self.ir.get('enums', {})
        self.functions = self.ir.get('functions', {})
        self.types = self.ir.get('types', {})
        self.constants = self.ir.get('constants', {})

        # Output buffers
        self.cdef_lines = []  # cffi C declarations
        self.py_lines = []    # Python code

    def is_valid_c_identifier(self, name: str) -> bool:
        """Check if a name is a valid C identifier

        Excludes names containing:
        - Dot (.)
        - Asterisk (*)
        - Space
        - const and other modifiers
        """
        if not name:
            return False
        # Names with special characters are not valid identifiers
        if any(c in name for c in ['.', '*', ' ', '[', ']']):
            return False
        # Skip names with const/volatile modifiers
        if 'const' in name or 'volatile' in name:
            return False
        return True

    def to_python_name(self, c_name: str) -> str:
        """Convert C naming to Python class name
        Example: ufbx_scene -> Scene
        """
        if c_name.startswith('ufbx_'):
            c_name = c_name[5:]
        # Convert to PascalCase
        parts = c_name.split('_')
        return ''.join(word.capitalize() for word in parts)

    def generate_cdef(self):
        """Generate cffi cdef declarations"""
        self.cdef_lines.append('// Auto-generated cffi declarations for ufbx')
        self.cdef_lines.append('// Do not edit manually')
        self.cdef_lines.append('')

        # Basic type definitions
        self.cdef_lines.append('// Basic types')
        self.cdef_lines.append('typedef double ufbx_real;')
        self.cdef_lines.append('typedef bool ufbx_bool;')
        self.cdef_lines.append('typedef uint64_t ufbx_id;')
        self.cdef_lines.append('')

        # Generate enums
        for enum_name, enum_data in self.enums.items():
            self.emit_enum_cdef(enum_name, enum_data)

        # Generate struct forward declarations (only valid C identifiers)
        for struct_name in self.structs.keys():
            if self.is_valid_c_identifier(struct_name):
                self.cdef_lines.append(f'typedef struct {struct_name} {struct_name};')
        self.cdef_lines.append('')

        # Generate full definitions for critical structs
        self.emit_critical_structs()

        # Other struct definitions (use ... to let cffi auto-deduce)
        for struct_name, struct_data in self.structs.items():
            if self.is_valid_c_identifier(struct_name) and struct_name not in self.get_critical_struct_names():
                self.emit_struct_cdef(struct_name, struct_data)

        # Generate key function declarations
        # cffi requires explicit function declarations in cdef for Python access
        self.emit_key_functions()

    def emit_enum_cdef(self, name: str, data: dict):
        """Generate cdef declaration for enum"""
        self.cdef_lines.append(f'typedef enum {name} {{')
        for value_name in data.get('values', []):
            self.cdef_lines.append(f'    {value_name},')
        self.cdef_lines.append(f'}} {name};')
        self.cdef_lines.append('')

    def get_critical_struct_names(self):
        """Return names of critical structs that need full definitions"""
        return {'ufbx_error', 'ufbx_string'}

    def emit_critical_structs(self):
        """Generate full definitions for critical structs"""
        self.cdef_lines.append('// Critical structs with full definitions')
        self.cdef_lines.append('')

        # ufbx_string
        self.cdef_lines.append('struct ufbx_string {')
        self.cdef_lines.append('    const char *data;')
        self.cdef_lines.append('    size_t length;')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

        # ufbx_error
        self.cdef_lines.append('struct ufbx_error {')
        self.cdef_lines.append('    ufbx_error_type type;')
        self.cdef_lines.append('    ufbx_string description;')
        self.cdef_lines.append('    ...; // Other fields')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

    def emit_struct_cdef(self, name: str, data: dict):
        """Generate cdef declaration for struct (simplified using ...)"""
        # cffi supports "..." to let the compiler auto-deduce struct
        self.cdef_lines.append(f'struct {name} {{ ...; }};')
        self.cdef_lines.append('')

    def emit_key_functions(self):
        """Generate key function declarations (manually list core API)"""
        self.cdef_lines.append('')
        self.cdef_lines.append('// Core API functions')

        # Scene loading/freeing
        self.cdef_lines.append('ufbx_scene* ufbx_load_file(const char *filename, const ufbx_load_opts *opts, ufbx_error *error);')
        self.cdef_lines.append('ufbx_scene* ufbx_load_file_len(const char *filename, size_t filename_len, const ufbx_load_opts *opts, ufbx_error *error);')
        self.cdef_lines.append('ufbx_scene* ufbx_load_memory(const void *data, size_t data_size, const ufbx_load_opts *opts, ufbx_error *error);')
        self.cdef_lines.append('void ufbx_free_scene(ufbx_scene *scene);')
        self.cdef_lines.append('')

        # Animation evaluation
        self.cdef_lines.append('ufbx_real ufbx_evaluate_curve(const ufbx_anim_curve *curve, double time, ufbx_real default_value);')
        self.cdef_lines.append('ufbx_transform ufbx_evaluate_transform(const ufbx_anim *anim, const ufbx_node *node, double time);')
        self.cdef_lines.append('')

        # Utility functions
        self.cdef_lines.append('size_t ufbx_generate_indices(const ufbx_vertex_stream *streams, size_t num_streams, uint32_t *indices, size_t num_indices, const ufbx_allocator_opts *allocator, ufbx_error *error);')
        self.cdef_lines.append('uint32_t ufbx_triangulate_face(uint32_t *indices, size_t num_indices, const ufbx_mesh *mesh, ufbx_face face);')
        self.cdef_lines.append('')

    def generate_python(self):
        """Generate Python binding code"""
        self.py_lines.append('"""')
        self.py_lines.append('Auto-generated ufbx Python bindings')
        self.py_lines.append('Do not edit manually')
        self.py_lines.append('"""')
        self.py_lines.append('')
        self.py_lines.append('from ufbx._ufbx import ffi, lib')
        self.py_lines.append('from enum import IntEnum')
        self.py_lines.append('from typing import Optional, List')
        self.py_lines.append('')

        # Generate enum classes
        for enum_name, enum_data in self.enums.items():
            self.emit_enum_python(enum_name, enum_data)

        # Generate struct wrapper classes (simplified, only main ones)
        important_structs = ['ufbx_scene', 'ufbx_mesh', 'ufbx_node', 'ufbx_error']
        for struct_name in important_structs:
            if struct_name in self.structs:
                self.emit_struct_python(struct_name, self.structs[struct_name])

    def emit_enum_python(self, name: str, data: dict):
        """Generate Python enum class"""
        class_name = self.to_python_name(name)
        self.py_lines.append(f'class {class_name}(IntEnum):')
        self.py_lines.append(f'    """Auto-generated from {name}"""')

        values = data.get('values', [])
        if not values:
            self.py_lines.append('    pass')
        else:
            for value_name in values:
                # Remove UFBX_ prefix
                py_name = value_name
                if py_name.startswith('UFBX_'):
                    py_name = py_name[5:]
                self.py_lines.append(f'    {py_name} = lib.{value_name}')

        self.py_lines.append('')

    def emit_struct_python(self, name: str, data: dict):
        """Generate Python struct wrapper class (simplified)"""
        class_name = self.to_python_name(name)
        self.py_lines.append(f'class {class_name}:')
        self.py_lines.append(f'    """Wrapper for {name}"""')
        self.py_lines.append(f'    def __init__(self, c_ptr):')
        self.py_lines.append(f'        self._ptr = c_ptr')
        self.py_lines.append('')

        # Add some basic properties (simplified)
        if name == 'ufbx_scene':
            self.py_lines.append('    @property')
            self.py_lines.append('    def metadata(self):')
            self.py_lines.append('        return self._ptr.metadata')
            self.py_lines.append('')

        self.py_lines.append('')

    def write_files(self, output_dir: str):
        """Write generated files"""
        # Write cdef declarations
        cdef_path = os.path.join(output_dir, 'ufbx', '_ufbx_cdef.h')
        os.makedirs(os.path.dirname(cdef_path), exist_ok=True)
        with open(cdef_path, 'w') as f:
            f.write('\n'.join(self.cdef_lines))
        print(f'Generated: {cdef_path}')

        # Write Python code
        py_path = os.path.join(output_dir, 'ufbx', 'generated.py')
        with open(py_path, 'w') as f:
            f.write('\n'.join(self.py_lines))
        print(f'Generated: {py_path}')

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.dirname(script_dir)
    ir_path = os.path.join(script_dir, 'build', 'ufbx_typed.json')

    if not os.path.exists(ir_path):
        print(f'Error: IR file not found: {ir_path}', file=sys.stderr)
        print('Please run: python3 bindgen/ufbx_parser.py -i ufbx-c/ufbx.h -o bindgen/build/ufbx.json', file=sys.stderr)
        print('         python3 bindgen/ufbx_ir.py', file=sys.stderr)
        sys.exit(1)

    print(f'Reading IR from: {ir_path}')
    generator = PythonGenerator(ir_path)

    print('Generating cffi declarations...')
    generator.generate_cdef()

    print('Generating Python bindings...')
    generator.generate_python()

    print('Writing output files...')
    generator.write_files(project_dir)

    print('Done!')

if __name__ == '__main__':
    main()
