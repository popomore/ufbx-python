#!/usr/bin/env python3
"""
Python binding generator for ufbx

Based on the implementation of generate_rust.py, generates Python (cffi) bindings for ufbx
"""

import json
import os
import sys


class PythonGenerator:
    def __init__(self, ir_path: str):
        with open(ir_path) as f:
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
        return not ('const' in name or 'volatile' in name)

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
        for struct_name in self.structs:
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
        return {
            'ufbx_error', 'ufbx_string',
            'ufbx_vec2', 'ufbx_vec3', 'ufbx_vec4',
            'ufbx_quat', 'ufbx_matrix', 'ufbx_transform'
        }

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

        # ufbx_vec2
        self.cdef_lines.append('struct ufbx_vec2 {')
        self.cdef_lines.append('    ufbx_real x, y;')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

        # ufbx_vec3
        self.cdef_lines.append('struct ufbx_vec3 {')
        self.cdef_lines.append('    ufbx_real x, y, z;')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

        # ufbx_vec4
        self.cdef_lines.append('struct ufbx_vec4 {')
        self.cdef_lines.append('    ufbx_real x, y, z, w;')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

        # ufbx_quat
        self.cdef_lines.append('struct ufbx_quat {')
        self.cdef_lines.append('    ufbx_real x, y, z, w;')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

        # ufbx_matrix
        self.cdef_lines.append('struct ufbx_matrix {')
        self.cdef_lines.append('    ufbx_real m00, m10, m20;')
        self.cdef_lines.append('    ufbx_real m01, m11, m21;')
        self.cdef_lines.append('    ufbx_real m02, m12, m22;')
        self.cdef_lines.append('    ufbx_real m03, m13, m23;')
        self.cdef_lines.append('};')
        self.cdef_lines.append('')

        # ufbx_transform
        self.cdef_lines.append('struct ufbx_transform {')
        self.cdef_lines.append('    ufbx_vec3 translation;')
        self.cdef_lines.append('    ufbx_quat rotation;')
        self.cdef_lines.append('    ufbx_vec3 scale;')
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
        self.cdef_lines.append('void ufbx_retain_scene(ufbx_scene *scene);')
        self.cdef_lines.append('')

        # Animation evaluation
        self.cdef_lines.append('ufbx_real ufbx_evaluate_curve(const ufbx_anim_curve *curve, double time, ufbx_real default_value);')
        self.cdef_lines.append('ufbx_transform ufbx_evaluate_transform(const ufbx_anim *anim, const ufbx_node *node, double time);')
        self.cdef_lines.append('ufbx_scene* ufbx_evaluate_scene(const ufbx_scene *scene, const ufbx_anim *anim, double time, const ufbx_evaluate_opts *opts, ufbx_error *error);')
        self.cdef_lines.append('')

        # Property queries
        self.cdef_lines.append('ufbx_prop* ufbx_find_prop_len(const ufbx_props *props, const char *name, size_t name_len);')
        self.cdef_lines.append('ufbx_real ufbx_find_real(const ufbx_props *props, const char *name, ufbx_real def);')
        self.cdef_lines.append('ufbx_vec3 ufbx_find_vec3(const ufbx_props *props, const char *name, ufbx_vec3 def);')
        self.cdef_lines.append('int64_t ufbx_find_int(const ufbx_props *props, const char *name, int64_t def);')
        self.cdef_lines.append('bool ufbx_find_bool(const ufbx_props *props, const char *name, bool def);')
        self.cdef_lines.append('ufbx_string ufbx_find_string(const ufbx_props *props, const char *name, ufbx_string def);')
        self.cdef_lines.append('')

        # Element queries
        self.cdef_lines.append('ufbx_element* ufbx_find_element_len(const ufbx_scene *scene, ufbx_element_type type, const char *name, size_t name_len);')
        self.cdef_lines.append('ufbx_node* ufbx_find_node_len(const ufbx_scene *scene, const char *name, size_t name_len);')
        self.cdef_lines.append('ufbx_anim_stack* ufbx_find_anim_stack_len(const ufbx_scene *scene, const char *name, size_t name_len);')
        self.cdef_lines.append('ufbx_material* ufbx_find_material_len(const ufbx_scene *scene, const char *name, size_t name_len);')
        self.cdef_lines.append('')

        # Type casting
        for element_type in ['node', 'mesh', 'light', 'camera', 'bone', 'material', 'texture',
                             'anim_stack', 'anim_layer', 'anim_curve', 'skin_deformer', 'blend_deformer']:
            self.cdef_lines.append(f'ufbx_{element_type}* ufbx_as_{element_type}(const ufbx_element *element);')
        self.cdef_lines.append('')

        # Mesh operations
        self.cdef_lines.append('size_t ufbx_generate_indices(const ufbx_vertex_stream *streams, size_t num_streams, uint32_t *indices, size_t num_indices, const ufbx_allocator_opts *allocator, ufbx_error *error);')
        self.cdef_lines.append('uint32_t ufbx_triangulate_face(uint32_t *indices, size_t num_indices, const ufbx_mesh *mesh, ufbx_face face);')
        self.cdef_lines.append('ufbx_mesh* ufbx_subdivide_mesh(const ufbx_mesh *mesh, size_t level, const ufbx_subdivide_opts *opts, ufbx_error *error);')
        self.cdef_lines.append('void ufbx_free_mesh(ufbx_mesh *mesh);')
        self.cdef_lines.append('')

        # Math operations
        self.cdef_lines.append('ufbx_vec3 ufbx_vec3_normalize(ufbx_vec3 v);')
        self.cdef_lines.append('ufbx_quat ufbx_quat_mul(ufbx_quat a, ufbx_quat b);')
        self.cdef_lines.append('ufbx_quat ufbx_quat_normalize(ufbx_quat q);')
        self.cdef_lines.append('ufbx_matrix ufbx_matrix_mul(const ufbx_matrix *a, const ufbx_matrix *b);')
        self.cdef_lines.append('ufbx_matrix ufbx_matrix_invert(const ufbx_matrix *m);')
        self.cdef_lines.append('ufbx_vec3 ufbx_transform_position(const ufbx_matrix *m, ufbx_vec3 v);')
        self.cdef_lines.append('ufbx_vec3 ufbx_transform_direction(const ufbx_matrix *m, ufbx_vec3 v);')
        self.cdef_lines.append('ufbx_matrix ufbx_transform_to_matrix(const ufbx_transform *t);')
        self.cdef_lines.append('ufbx_transform ufbx_matrix_to_transform(const ufbx_matrix *m);')
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
        self.py_lines.append('from typing import Optional, List, Tuple')
        self.py_lines.append('')

        # Generate enum classes
        for enum_name, enum_data in self.enums.items():
            self.emit_enum_python(enum_name, enum_data)

        # Generate struct wrapper classes - all important element types
        important_structs = [
            # Core
            'ufbx_scene', 'ufbx_element', 'ufbx_error',
            # Nodes and hierarchy
            'ufbx_node',
            # Geometry
            'ufbx_mesh', 'ufbx_line_curve', 'ufbx_nurbs_curve', 'ufbx_nurbs_surface',
            # Lights and cameras
            'ufbx_light', 'ufbx_camera', 'ufbx_bone',
            # Materials
            'ufbx_material', 'ufbx_texture', 'ufbx_video', 'ufbx_shader',
            # Animation
            'ufbx_anim', 'ufbx_anim_stack', 'ufbx_anim_layer', 'ufbx_anim_curve', 'ufbx_anim_value',
            # Deformers
            'ufbx_skin_deformer', 'ufbx_skin_cluster',
            'ufbx_blend_deformer', 'ufbx_blend_channel', 'ufbx_blend_shape',
            'ufbx_cache_deformer', 'ufbx_cache_file', 'ufbx_geometry_cache',
            # Constraints
            'ufbx_constraint',
            # Collections
            'ufbx_display_layer', 'ufbx_selection_set', 'ufbx_character',
            # Data types
            'ufbx_props', 'ufbx_prop',
            # Math types
            'ufbx_vec2', 'ufbx_vec3', 'ufbx_vec4', 'ufbx_quat', 'ufbx_matrix', 'ufbx_transform',
        ]
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
        self.py_lines.append('    def __init__(self, c_ptr):')
        self.py_lines.append('        self._ptr = c_ptr')
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
