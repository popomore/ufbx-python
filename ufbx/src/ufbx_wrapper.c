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

int ufbx_wrapper_scene_get_axes_right(const ufbx_scene *scene) {
    return scene ? (int)scene->settings.axes.right : (int)UFBX_COORDINATE_AXIS_UNKNOWN;
}

int ufbx_wrapper_scene_get_axes_up(const ufbx_scene *scene) {
    return scene ? (int)scene->settings.axes.up : (int)UFBX_COORDINATE_AXIS_UNKNOWN;
}

int ufbx_wrapper_scene_get_axes_front(const ufbx_scene *scene) {
    return scene ? (int)scene->settings.axes.front : (int)UFBX_COORDINATE_AXIS_UNKNOWN;
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

// Light access
size_t ufbx_wrapper_scene_get_num_lights(const ufbx_scene *scene) {
    return scene ? scene->lights.count : 0;
}

ufbx_light* ufbx_wrapper_scene_get_light(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->lights.count) return NULL;
    return scene->lights.data[index];
}

ufbx_light* ufbx_wrapper_node_get_light(const ufbx_node *node) {
    return node ? node->light : NULL;
}

const char* ufbx_wrapper_light_get_name(const ufbx_light *light) {
    if (!light) return "";
    return light->name.data ? light->name.data : "";
}

void ufbx_wrapper_light_get_color(const ufbx_light *light, float *rgb) {
    if (!light || !rgb) return;
    rgb[0] = (float)light->color.x;
    rgb[1] = (float)light->color.y;
    rgb[2] = (float)light->color.z;
}

double ufbx_wrapper_light_get_intensity(const ufbx_light *light) {
    return light ? light->intensity : 0.0;
}

void ufbx_wrapper_light_get_local_direction(const ufbx_light *light, float *xyz) {
    if (!light || !xyz) return;
    xyz[0] = (float)light->local_direction.x;
    xyz[1] = (float)light->local_direction.y;
    xyz[2] = (float)light->local_direction.z;
}

int ufbx_wrapper_light_get_type(const ufbx_light *light) {
    return light ? (int)light->type : 0;
}

int ufbx_wrapper_light_get_decay(const ufbx_light *light) {
    return light ? (int)light->decay : 0;
}

int ufbx_wrapper_light_get_area_shape(const ufbx_light *light) {
    return light ? (int)light->area_shape : 0;
}

double ufbx_wrapper_light_get_inner_angle(const ufbx_light *light) {
    return light ? light->inner_angle : 0.0;
}

double ufbx_wrapper_light_get_outer_angle(const ufbx_light *light) {
    return light ? light->outer_angle : 0.0;
}

bool ufbx_wrapper_light_get_cast_light(const ufbx_light *light) {
    return light ? light->cast_light : false;
}

bool ufbx_wrapper_light_get_cast_shadows(const ufbx_light *light) {
    return light ? light->cast_shadows : false;
}

// Camera access
size_t ufbx_wrapper_scene_get_num_cameras(const ufbx_scene *scene) {
    return scene ? scene->cameras.count : 0;
}

ufbx_camera* ufbx_wrapper_scene_get_camera(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->cameras.count) return NULL;
    return scene->cameras.data[index];
}

ufbx_camera* ufbx_wrapper_node_get_camera(const ufbx_node *node) {
    return node ? node->camera : NULL;
}

const char* ufbx_wrapper_camera_get_name(const ufbx_camera *camera) {
    if (!camera) return "";
    return camera->name.data ? camera->name.data : "";
}

int ufbx_wrapper_camera_get_projection_mode(const ufbx_camera *camera) {
    return camera ? (int)camera->projection_mode : 0;
}

void ufbx_wrapper_camera_get_resolution(const ufbx_camera *camera, float *xy) {
    if (!camera || !xy) return;
    xy[0] = (float)camera->resolution.x;
    xy[1] = (float)camera->resolution.y;
}

bool ufbx_wrapper_camera_get_resolution_is_pixels(const ufbx_camera *camera) {
    return camera ? camera->resolution_is_pixels : false;
}

void ufbx_wrapper_camera_get_field_of_view_deg(const ufbx_camera *camera, float *xy) {
    if (!camera || !xy) return;
    xy[0] = (float)camera->field_of_view_deg.x;
    xy[1] = (float)camera->field_of_view_deg.y;
}

void ufbx_wrapper_camera_get_field_of_view_tan(const ufbx_camera *camera, float *xy) {
    if (!camera || !xy) return;
    xy[0] = (float)camera->field_of_view_tan.x;
    xy[1] = (float)camera->field_of_view_tan.y;
}

double ufbx_wrapper_camera_get_orthographic_extent(const ufbx_camera *camera) {
    return camera ? camera->orthographic_extent : 0.0;
}

void ufbx_wrapper_camera_get_orthographic_size(const ufbx_camera *camera, float *xy) {
    if (!camera || !xy) return;
    xy[0] = (float)camera->orthographic_size.x;
    xy[1] = (float)camera->orthographic_size.y;
}

double ufbx_wrapper_camera_get_aspect_ratio(const ufbx_camera *camera) {
    return camera ? camera->aspect_ratio : 1.0;
}

double ufbx_wrapper_camera_get_near_plane(const ufbx_camera *camera) {
    return camera ? camera->near_plane : 0.0;
}

double ufbx_wrapper_camera_get_far_plane(const ufbx_camera *camera) {
    return camera ? camera->far_plane : 0.0;
}

// Bone access
size_t ufbx_wrapper_scene_get_num_bones(const ufbx_scene *scene) {
    return scene ? scene->bones.count : 0;
}

ufbx_bone* ufbx_wrapper_scene_get_bone(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->bones.count) return NULL;
    return scene->bones.data[index];
}

ufbx_bone* ufbx_wrapper_node_get_bone(const ufbx_node *node) {
    return node ? node->bone : NULL;
}

const char* ufbx_wrapper_bone_get_name(const ufbx_bone *bone) {
    if (!bone) return "";
    return bone->name.data ? bone->name.data : "";
}

double ufbx_wrapper_bone_get_radius(const ufbx_bone *bone) {
    return bone ? bone->radius : 0.0;
}

double ufbx_wrapper_bone_get_relative_length(const ufbx_bone *bone) {
    return bone ? bone->relative_length : 0.0;
}

bool ufbx_wrapper_bone_is_root(const ufbx_bone *bone) {
    return bone ? bone->is_root : false;
}

// Texture access
size_t ufbx_wrapper_scene_get_num_textures(const ufbx_scene *scene) {
    return scene ? scene->textures.count : 0;
}

ufbx_texture* ufbx_wrapper_scene_get_texture(const ufbx_scene *scene, size_t index) {
    if (!scene || index >= scene->textures.count) return NULL;
    return scene->textures.data[index];
}

const char* ufbx_wrapper_texture_get_name(const ufbx_texture *texture) {
    if (!texture) return "";
    return texture->name.data ? texture->name.data : "";
}

const char* ufbx_wrapper_texture_get_filename(const ufbx_texture *texture) {
    if (!texture) return "";
    return texture->filename.data ? texture->filename.data : "";
}

const char* ufbx_wrapper_texture_get_absolute_filename(const ufbx_texture *texture) {
    if (!texture) return "";
    return texture->absolute_filename.data ? texture->absolute_filename.data : "";
}

const char* ufbx_wrapper_texture_get_relative_filename(const ufbx_texture *texture) {
    if (!texture) return "";
    return texture->relative_filename.data ? texture->relative_filename.data : "";
}

int ufbx_wrapper_texture_get_type(const ufbx_texture *texture) {
    return texture ? (int)texture->type : 0;
}
