#include "ufbx_wrapper.h"
#include "ufbx-c/ufbx.h"
#include <string.h>
#include <stdlib.h>

// Scene management
ufbx_scene* ufbx_wrapper_load_file(const char *filename, char **error_msg) {
    ufbx_load_opts opts = {0};
    ufbx_error error;
    ufbx_scene *scene = ufbx_load_file(filename, &opts, &error);

    if (!scene && error_msg) {
        size_t len = error.description.length;
        *error_msg = (char*)malloc(len + 1);
        if (*error_msg) {
            memcpy(*error_msg, error.description.data, len);
            (*error_msg)[len] = '\0';
        }
    }

    return scene;
}

void ufbx_wrapper_free_scene(ufbx_scene *scene) {
    if (scene) {
        ufbx_free_scene(scene);
    }
}

// Scene queries
size_t ufbx_wrapper_scene_get_num_nodes(const ufbx_scene *scene) {
    return scene ? scene->nodes.count : 0;
}

size_t ufbx_wrapper_scene_get_num_meshes(const ufbx_scene *scene) {
    return scene ? scene->meshes.count : 0;
}

size_t ufbx_wrapper_scene_get_num_materials(const ufbx_scene *scene) {
    return scene ? scene->materials.count : 0;
}

ufbx_node* ufbx_wrapper_scene_get_root_node(const ufbx_scene *scene) {
    return scene ? scene->root_node : NULL;
}

// Node access
ufbx_node* ufbx_wrapper_scene_get_node(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->nodes.count) return NULL;
    return scene->nodes.data[index];
}

const char* ufbx_wrapper_node_get_name(const ufbx_node *node) {
    if (!node) return "";
    return node->name.data ? node->name.data : "";
}

size_t ufbx_wrapper_node_get_num_children(const ufbx_node *node) {
    return node ? node->children.count : 0;
}

ufbx_node* ufbx_wrapper_node_get_child(const ufbx_node *node, size_t index) {
    if (!node || index >= node->children.count) return NULL;
    return node->children.data[index];
}

ufbx_node* ufbx_wrapper_node_get_parent(const ufbx_node *node) {
    return node ? node->parent : NULL;
}

ufbx_mesh* ufbx_wrapper_node_get_mesh(const ufbx_node *node) {
    return node ? node->mesh : NULL;
}

bool ufbx_wrapper_node_is_root(const ufbx_node *node) {
    return node ? node->is_root : false;
}

// Node transform
void ufbx_wrapper_node_get_world_transform(const ufbx_node *node, double *matrix16) {
    if (!node || !matrix16) return;

    const ufbx_matrix *m = &node->node_to_world;
    // Column-major order
    matrix16[0] = m->m00; matrix16[4] = m->m01; matrix16[8]  = m->m02; matrix16[12] = m->m03;
    matrix16[1] = m->m10; matrix16[5] = m->m11; matrix16[9]  = m->m12; matrix16[13] = m->m13;
    matrix16[2] = m->m20; matrix16[6] = m->m21; matrix16[10] = m->m22; matrix16[14] = m->m23;
    matrix16[3] = 0.0;    matrix16[7] = 0.0;    matrix16[11] = 0.0;    matrix16[15] = 1.0;
}

void ufbx_wrapper_node_get_local_transform(const ufbx_node *node, double *matrix16) {
    if (!node || !matrix16) return;

    const ufbx_matrix *m = &node->node_to_parent;
    // Column-major order
    matrix16[0] = m->m00; matrix16[4] = m->m01; matrix16[8]  = m->m02; matrix16[12] = m->m03;
    matrix16[1] = m->m10; matrix16[5] = m->m11; matrix16[9]  = m->m12; matrix16[13] = m->m13;
    matrix16[2] = m->m20; matrix16[6] = m->m21; matrix16[10] = m->m22; matrix16[14] = m->m23;
    matrix16[3] = 0.0;    matrix16[7] = 0.0;    matrix16[11] = 0.0;    matrix16[15] = 1.0;
}

// Mesh access
ufbx_mesh* ufbx_wrapper_scene_get_mesh(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->meshes.count) return NULL;
    return scene->meshes.data[index];
}

const char* ufbx_wrapper_mesh_get_name(const ufbx_mesh *mesh) {
    if (!mesh) return "";
    return mesh->name.data ? mesh->name.data : "";
}

size_t ufbx_wrapper_mesh_get_num_vertices(const ufbx_mesh *mesh) {
    return mesh ? mesh->num_vertices : 0;
}

size_t ufbx_wrapper_mesh_get_num_indices(const ufbx_mesh *mesh) {
    return mesh ? mesh->num_indices : 0;
}

size_t ufbx_wrapper_mesh_get_num_faces(const ufbx_mesh *mesh) {
    return mesh ? mesh->num_faces : 0;
}

size_t ufbx_wrapper_mesh_get_num_triangles(const ufbx_mesh *mesh) {
    return mesh ? mesh->num_triangles : 0;
}

// Mesh vertex data
const float* ufbx_wrapper_mesh_get_vertex_positions(const ufbx_mesh *mesh, size_t *out_count) {
    if (!mesh || !mesh->vertex_position.exists || !out_count) {
        if (out_count) *out_count = 0;
        return NULL;
    }

    *out_count = mesh->vertex_position.values.count;
    return (const float*)mesh->vertex_position.values.data;
}

const float* ufbx_wrapper_mesh_get_vertex_normals(const ufbx_mesh *mesh, size_t *out_count) {
    if (!mesh || !mesh->vertex_normal.exists || !out_count) {
        if (out_count) *out_count = 0;
        return NULL;
    }

    *out_count = mesh->vertex_normal.values.count;
    return (const float*)mesh->vertex_normal.values.data;
}

const float* ufbx_wrapper_mesh_get_vertex_uvs(const ufbx_mesh *mesh, size_t *out_count) {
    if (!mesh || !mesh->vertex_uv.exists || !out_count) {
        if (out_count) *out_count = 0;
        return NULL;
    }

    *out_count = mesh->vertex_uv.values.count;
    return (const float*)mesh->vertex_uv.values.data;
}

const uint32_t* ufbx_wrapper_mesh_get_indices(const ufbx_mesh *mesh, size_t *out_count) {
    if (!mesh || !mesh->vertex_position.exists || !out_count) {
        if (out_count) *out_count = 0;
        return NULL;
    }

    *out_count = mesh->vertex_position.indices.count;
    return mesh->vertex_position.indices.data;
}

// Material access
ufbx_material* ufbx_wrapper_scene_get_material(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->materials.count) return NULL;
    return scene->materials.data[index];
}

size_t ufbx_wrapper_mesh_get_num_materials(const ufbx_mesh *mesh) {
    return mesh ? mesh->materials.count : 0;
}

ufbx_material* ufbx_wrapper_mesh_get_material(const ufbx_mesh *mesh, size_t index) {
    if (!mesh || index >= mesh->materials.count) return NULL;
    return mesh->materials.data[index];
}

const char* ufbx_wrapper_material_get_name(const ufbx_material *material) {
    if (!material) return "";
    return material->name.data ? material->name.data : "";
}
