#ifndef UFBX_WRAPPER_H
#define UFBX_WRAPPER_H

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// Opaque handles
typedef struct ufbx_scene ufbx_scene;
typedef struct ufbx_mesh ufbx_mesh;
typedef struct ufbx_node ufbx_node;
typedef struct ufbx_material ufbx_material;
typedef struct ufbx_texture ufbx_texture;

// Scene management
ufbx_scene* ufbx_wrapper_load_file(const char *filename, char **error_msg);
void ufbx_wrapper_free_scene(ufbx_scene *scene);

// Scene queries
size_t ufbx_wrapper_scene_get_num_nodes(const ufbx_scene *scene);
size_t ufbx_wrapper_scene_get_num_meshes(const ufbx_scene *scene);
size_t ufbx_wrapper_scene_get_num_materials(const ufbx_scene *scene);
ufbx_node* ufbx_wrapper_scene_get_root_node(const ufbx_scene *scene);

// Scene settings.axes (CoordinateAxis: 0-6)
int ufbx_wrapper_scene_get_axes_right(const ufbx_scene *scene);
int ufbx_wrapper_scene_get_axes_up(const ufbx_scene *scene);
int ufbx_wrapper_scene_get_axes_front(const ufbx_scene *scene);

// Node access
ufbx_node* ufbx_wrapper_scene_get_node(const ufbx_scene *scene, size_t index);
const char* ufbx_wrapper_node_get_name(const ufbx_node *node);
size_t ufbx_wrapper_node_get_num_children(const ufbx_node *node);
ufbx_node* ufbx_wrapper_node_get_child(const ufbx_node *node, size_t index);
ufbx_node* ufbx_wrapper_node_get_parent(const ufbx_node *node);
ufbx_mesh* ufbx_wrapper_node_get_mesh(const ufbx_node *node);
bool ufbx_wrapper_node_is_root(const ufbx_node *node);

// Node transform (4x4 matrix stored in column-major order)
void ufbx_wrapper_node_get_world_transform(const ufbx_node *node, double *matrix16);
void ufbx_wrapper_node_get_local_transform(const ufbx_node *node, double *matrix16);

// Mesh access
ufbx_mesh* ufbx_wrapper_scene_get_mesh(const ufbx_scene *scene, size_t index);
const char* ufbx_wrapper_mesh_get_name(const ufbx_mesh *mesh);
size_t ufbx_wrapper_mesh_get_num_vertices(const ufbx_mesh *mesh);
size_t ufbx_wrapper_mesh_get_num_indices(const ufbx_mesh *mesh);
size_t ufbx_wrapper_mesh_get_num_faces(const ufbx_mesh *mesh);
size_t ufbx_wrapper_mesh_get_num_triangles(const ufbx_mesh *mesh);

// Mesh vertex data (returns pointers to internal data - valid while scene lives)
const float* ufbx_wrapper_mesh_get_vertex_positions(const ufbx_mesh *mesh, size_t *out_count);
const float* ufbx_wrapper_mesh_get_vertex_normals(const ufbx_mesh *mesh, size_t *out_count);
const float* ufbx_wrapper_mesh_get_vertex_uvs(const ufbx_mesh *mesh, size_t *out_count);
const uint32_t* ufbx_wrapper_mesh_get_indices(const ufbx_mesh *mesh, size_t *out_count);

// Material access
ufbx_material* ufbx_wrapper_scene_get_material(const ufbx_scene *scene, size_t index);
size_t ufbx_wrapper_mesh_get_num_materials(const ufbx_mesh *mesh);
ufbx_material* ufbx_wrapper_mesh_get_material(const ufbx_mesh *mesh, size_t index);
const char* ufbx_wrapper_material_get_name(const ufbx_material *material);

#ifdef __cplusplus
}
#endif

#endif // UFBX_WRAPPER_H
