# cython: language_level=3
"""
Cython bindings for ufbx - thin wrapper around C API
"""
from libc.stdlib cimport free
from libc.stdint cimport uint32_t
import numpy as np
cimport numpy as np

np.import_array()

# C declarations
cdef extern from "ufbx_wrapper.h":
    ctypedef struct ufbx_scene:
        pass
    ctypedef struct ufbx_mesh:
        pass
    ctypedef struct ufbx_node:
        pass
    ctypedef struct ufbx_material:
        pass

    # Scene management
    ufbx_scene* ufbx_wrapper_load_file(const char *filename, char **error_msg)
    void ufbx_wrapper_free_scene(ufbx_scene *scene)

    # Scene queries
    size_t ufbx_wrapper_scene_get_num_nodes(const ufbx_scene *scene)
    size_t ufbx_wrapper_scene_get_num_meshes(const ufbx_scene *scene)
    size_t ufbx_wrapper_scene_get_num_materials(const ufbx_scene *scene)
    ufbx_node* ufbx_wrapper_scene_get_root_node(const ufbx_scene *scene)

    # Node access
    ufbx_node* ufbx_wrapper_scene_get_node(const ufbx_scene *scene, size_t index)
    const char* ufbx_wrapper_node_get_name(const ufbx_node *node)
    size_t ufbx_wrapper_node_get_num_children(const ufbx_node *node)
    ufbx_node* ufbx_wrapper_node_get_child(const ufbx_node *node, size_t index)
    ufbx_node* ufbx_wrapper_node_get_parent(const ufbx_node *node)
    ufbx_mesh* ufbx_wrapper_node_get_mesh(const ufbx_node *node)
    bint ufbx_wrapper_node_is_root(const ufbx_node *node)
    void ufbx_wrapper_node_get_world_transform(const ufbx_node *node, double *matrix16)
    void ufbx_wrapper_node_get_local_transform(const ufbx_node *node, double *matrix16)

    # Mesh access
    ufbx_mesh* ufbx_wrapper_scene_get_mesh(const ufbx_scene *scene, size_t index)
    const char* ufbx_wrapper_mesh_get_name(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_vertices(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_indices(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_faces(const ufbx_mesh *mesh)
    size_t ufbx_wrapper_mesh_get_num_triangles(const ufbx_mesh *mesh)

    # Mesh vertex data
    const float* ufbx_wrapper_mesh_get_vertex_positions(const ufbx_mesh *mesh, size_t *out_count)
    const float* ufbx_wrapper_mesh_get_vertex_normals(const ufbx_mesh *mesh, size_t *out_count)
    const float* ufbx_wrapper_mesh_get_vertex_uvs(const ufbx_mesh *mesh, size_t *out_count)
    const uint32_t* ufbx_wrapper_mesh_get_indices(const ufbx_mesh *mesh, size_t *out_count)

    # Material access
    ufbx_material* ufbx_wrapper_scene_get_material(const ufbx_scene *scene, size_t index)
    size_t ufbx_wrapper_mesh_get_num_materials(const ufbx_mesh *mesh)
    ufbx_material* ufbx_wrapper_mesh_get_material(const ufbx_mesh *mesh, size_t index)
    const char* ufbx_wrapper_material_get_name(const ufbx_material *material)


# Python classes
cdef class Scene:
    """FBX Scene - manages lifetime of all scene data"""
    cdef ufbx_scene* _scene
    cdef bint _closed

    def __cinit__(self):
        self._scene = NULL
        self._closed = False

    def __dealloc__(self):
        self.close()

    def close(self):
        """Free scene resources"""
        if self._scene != NULL and not self._closed:
            ufbx_wrapper_free_scene(self._scene)
            self._scene = NULL
            self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def nodes(self):
        """Get all nodes in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_nodes(self._scene)
        return [self._get_node(i) for i in range(count)]

    @property
    def meshes(self):
        """Get all meshes in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_meshes(self._scene)
        return [self._get_mesh(i) for i in range(count)]

    @property
    def materials(self):
        """Get all materials in the scene"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_scene_get_num_materials(self._scene)
        return [self._get_material(i) for i in range(count)]

    @property
    def root_node(self):
        """Get the root node"""
        if self._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_node* node = ufbx_wrapper_scene_get_root_node(self._scene)
        if node != NULL:
            return Node._create(self, node)
        return None

    cdef Node _get_node(self, size_t index):
        """Internal: get node by index"""
        cdef ufbx_node* node = ufbx_wrapper_scene_get_node(self._scene, index)
        if node != NULL:
            return Node._create(self, node)
        return None

    cdef Mesh _get_mesh(self, size_t index):
        """Internal: get mesh by index"""
        cdef ufbx_mesh* mesh = ufbx_wrapper_scene_get_mesh(self._scene, index)
        if mesh != NULL:
            return Mesh._create(self, mesh)
        return None

    cdef Material _get_material(self, size_t index):
        """Internal: get material by index"""
        cdef ufbx_material* material = ufbx_wrapper_scene_get_material(self._scene, index)
        if material != NULL:
            return Material._create(self, material)
        return None


cdef class Node:
    """Scene node with transform and hierarchy"""
    cdef Scene _scene
    cdef ufbx_node* _node

    @staticmethod
    cdef Node _create(Scene scene, ufbx_node* node):
        """Internal factory method"""
        cdef Node obj = Node.__new__(Node)
        obj._scene = scene
        obj._node = node
        return obj

    @property
    def name(self):
        """Node name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_node_get_name(self._node).decode('utf-8', errors='replace')

    @property
    def children(self):
        """Child nodes"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_node_get_num_children(self._node)
        cdef list result = []
        cdef ufbx_node* child
        for i in range(count):
            child = ufbx_wrapper_node_get_child(self._node, i)
            if child != NULL:
                result.append(Node._create(self._scene, child))
        return result

    @property
    def parent(self):
        """Parent node"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_node* parent = ufbx_wrapper_node_get_parent(self._node)
        if parent != NULL:
            return Node._create(self._scene, parent)
        return None

    @property
    def mesh(self):
        """Attached mesh"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef ufbx_mesh* mesh = ufbx_wrapper_node_get_mesh(self._node)
        if mesh != NULL:
            return Mesh._create(self._scene, mesh)
        return None

    @property
    def is_root(self):
        """Is this the root node"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_node_is_root(self._node)

    @property
    def world_transform(self):
        """World transform matrix (4x4, column-major)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef np.ndarray[np.float64_t, ndim=2] matrix = np.zeros((4, 4), dtype=np.float64)
        ufbx_wrapper_node_get_world_transform(self._node, <double*>matrix.data)
        return matrix

    @property
    def local_transform(self):
        """Local transform matrix (4x4, column-major)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef np.ndarray[np.float64_t, ndim=2] matrix = np.zeros((4, 4), dtype=np.float64)
        ufbx_wrapper_node_get_local_transform(self._node, <double*>matrix.data)
        return matrix


cdef class Mesh:
    """Polygonal mesh geometry"""
    cdef Scene _scene
    cdef ufbx_mesh* _mesh

    @staticmethod
    cdef Mesh _create(Scene scene, ufbx_mesh* mesh):
        """Internal factory method"""
        cdef Mesh obj = Mesh.__new__(Mesh)
        obj._scene = scene
        obj._mesh = mesh
        return obj

    @property
    def name(self):
        """Mesh name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_name(self._mesh).decode('utf-8', errors='replace')

    @property
    def num_vertices(self):
        """Number of vertices"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_vertices(self._mesh)

    @property
    def num_indices(self):
        """Number of indices"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_indices(self._mesh)

    @property
    def num_faces(self):
        """Number of faces"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_faces(self._mesh)

    @property
    def num_triangles(self):
        """Number of triangles"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_mesh_get_num_triangles(self._mesh)

    @property
    def vertex_positions(self):
        """Vertex positions as numpy array (N, 3)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const float* data = ufbx_wrapper_mesh_get_vertex_positions(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        # Create numpy array view (no copy) - valid while scene lives
        cdef np.npy_intp shape[2]
        shape[0] = <np.npy_intp>count
        shape[1] = 3
        return np.PyArray_SimpleNewFromData(2, shape, np.NPY_FLOAT32, <void*>data)

    @property
    def vertex_normals(self):
        """Vertex normals as numpy array (N, 3)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const float* data = ufbx_wrapper_mesh_get_vertex_normals(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        cdef np.npy_intp shape[2]
        shape[0] = <np.npy_intp>count
        shape[1] = 3
        return np.PyArray_SimpleNewFromData(2, shape, np.NPY_FLOAT32, <void*>data)

    @property
    def vertex_uvs(self):
        """Vertex UVs as numpy array (N, 2)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const float* data = ufbx_wrapper_mesh_get_vertex_uvs(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        cdef np.npy_intp shape[2]
        shape[0] = <np.npy_intp>count
        shape[1] = 2
        return np.PyArray_SimpleNewFromData(2, shape, np.NPY_FLOAT32, <void*>data)

    @property
    def indices(self):
        """Vertex indices as numpy array (N,)"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")

        cdef size_t count = 0
        cdef const uint32_t* data = ufbx_wrapper_mesh_get_indices(self._mesh, &count)

        if data == NULL or count == 0:
            return None

        cdef np.npy_intp shape[1]
        shape[0] = <np.npy_intp>count
        return np.PyArray_SimpleNewFromData(1, shape, np.NPY_UINT32, <void*>data)

    @property
    def materials(self):
        """Materials used by this mesh"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        cdef size_t count = ufbx_wrapper_mesh_get_num_materials(self._mesh)
        cdef list result = []
        cdef ufbx_material* material
        for i in range(count):
            material = ufbx_wrapper_mesh_get_material(self._mesh, i)
            if material != NULL:
                result.append(Material._create(self._scene, material))
        return result


cdef class Material:
    """Material definition"""
    cdef Scene _scene
    cdef ufbx_material* _material

    @staticmethod
    cdef Material _create(Scene scene, ufbx_material* material):
        """Internal factory method"""
        cdef Material obj = Material.__new__(Material)
        obj._scene = scene
        obj._material = material
        return obj

    @property
    def name(self):
        """Material name"""
        if self._scene._closed:
            raise RuntimeError("Scene is closed")
        return ufbx_wrapper_material_get_name(self._material).decode('utf-8', errors='replace')


# Module-level functions
def load_file(filename):
    """Load FBX file and return Scene object

    Args:
        filename: Path to FBX file

    Returns:
        Scene object

    Raises:
        RuntimeError: If loading fails
    """
    cdef char* error_msg = NULL
    cdef bytes filename_bytes = filename.encode('utf-8')
    cdef ufbx_scene* scene = ufbx_wrapper_load_file(filename_bytes, &error_msg)

    if scene == NULL:
        err = error_msg.decode('utf-8') if error_msg != NULL else "Unknown error"
        if error_msg != NULL:
            free(error_msg)
        raise RuntimeError(f"Failed to load FBX file: {err}")

    cdef Scene py_scene = Scene.__new__(Scene)
    py_scene._scene = scene
    py_scene._closed = False
    return py_scene
