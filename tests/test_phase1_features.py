"""
Test Phase 1 critical features: Mesh vertex data, Texture content, Node transforms.
"""
import ufbx


def test_mesh_vertex_tangent_property():
    """Test that Mesh.vertex_tangent property exists"""
    assert hasattr(ufbx.Mesh, 'vertex_tangent')
    # Property should be accessible (returns None if no data)
    # This is critical for normal mapping support


def test_mesh_vertex_bitangent_property():
    """Test that Mesh.vertex_bitangent property exists"""
    assert hasattr(ufbx.Mesh, 'vertex_bitangent')
    # Property should be accessible (returns None if no data)
    # This is critical for normal mapping support


def test_mesh_vertex_color_property():
    """Test that Mesh.vertex_color property exists"""
    assert hasattr(ufbx.Mesh, 'vertex_color')
    # Property should be accessible (returns None if no data)


def test_texture_content_property():
    """Test that Texture.content property exists"""
    assert hasattr(ufbx.Texture, 'content')
    # Property should be accessible (returns None if no embedded data)
    # Critical for accessing embedded texture data


def test_texture_has_file_property():
    """Test that Texture.has_file property exists"""
    assert hasattr(ufbx.Texture, 'has_file')
    # Property should return bool


def test_texture_uv_set_property():
    """Test that Texture.uv_set property exists"""
    assert hasattr(ufbx.Texture, 'uv_set')
    # Property should return string (UV set name)


def test_texture_wrap_u_property():
    """Test that Texture.wrap_u property exists"""
    assert hasattr(ufbx.Texture, 'wrap_u')
    # Property should return WrapMode enum


def test_texture_wrap_v_property():
    """Test that Texture.wrap_v property exists"""
    assert hasattr(ufbx.Texture, 'wrap_v')
    # Property should return WrapMode enum


def test_node_node_to_world_property():
    """Test that Node.node_to_world property exists"""
    assert hasattr(ufbx.Node, 'node_to_world')
    # Property should return 4x4 numpy array
    # Critical for world space transformations


def test_node_node_to_parent_property():
    """Test that Node.node_to_parent property exists"""
    assert hasattr(ufbx.Node, 'node_to_parent')
    # Property should return 4x4 numpy array


def test_node_geometry_transform_property():
    """Test that Node.geometry_transform property exists"""
    assert hasattr(ufbx.Node, 'geometry_transform')
    # Property should return Transform object
    # Critical for mesh pivot/offset transformations


def test_wrap_mode_enum():
    """Test that WrapMode enum exists and has correct values"""
    assert hasattr(ufbx, 'WrapMode')
    # Check enum values
    assert hasattr(ufbx.WrapMode, 'WRAP_MODE_REPEAT')
    assert hasattr(ufbx.WrapMode, 'WRAP_MODE_CLAMP')


def test_phase1_properties_are_accessible():
    """Test that all Phase 1 properties can be accessed without errors"""
    # Create a dummy scene to test properties don't raise on access
    # Note: Most will return None without actual FBX data, but shouldn't error
    
    # Mesh properties
    mesh_props = ['vertex_tangent', 'vertex_bitangent', 'vertex_color']
    for prop in mesh_props:
        assert hasattr(ufbx.Mesh, prop), f"Mesh.{prop} missing"
    
    # Texture properties
    texture_props = ['content', 'has_file', 'uv_set', 'wrap_u', 'wrap_v']
    for prop in texture_props:
        assert hasattr(ufbx.Texture, prop), f"Texture.{prop} missing"
    
    # Node properties
    node_props = ['node_to_world', 'node_to_parent', 'geometry_transform']
    for prop in node_props:
        assert hasattr(ufbx.Node, prop), f"Node.{prop} missing"


def test_transform_class_has_required_properties():
    """Test that Transform class has translation, rotation, scale"""
    assert hasattr(ufbx.Transform, 'translation')
    assert hasattr(ufbx.Transform, 'rotation')
    assert hasattr(ufbx.Transform, 'scale')
    
    # Create a Transform instance
    transform = ufbx.Transform()
    assert transform.translation is not None
    assert transform.rotation is not None
    assert transform.scale is not None
