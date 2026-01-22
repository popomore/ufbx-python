"""
Test animation and deformer API functionality
"""

import ufbx


def test_scene_has_animation_properties():
    """Test that Scene has animation-related properties"""
    assert hasattr(ufbx.Scene, 'anim_stacks')
    assert hasattr(ufbx.Scene, 'anim_curves')


def test_scene_has_deformer_properties():
    """Test that Scene has deformer-related properties"""
    assert hasattr(ufbx.Scene, 'skin_deformers')
    assert hasattr(ufbx.Scene, 'blend_deformers')
    assert hasattr(ufbx.Scene, 'blend_shapes')
    assert hasattr(ufbx.Scene, 'constraints')


def test_anim_stack_class_has_properties():
    """Test that AnimStack class has expected properties"""
    expected_properties = ['name', 'time_begin', 'time_end', 'layers']
    for prop in expected_properties:
        assert hasattr(ufbx.AnimStack, prop), f"AnimStack missing property: {prop}"


def test_anim_layer_class_has_properties():
    """Test that AnimLayer class has expected properties"""
    expected_properties = [
        'name', 'weight', 'weight_is_animated', 'blended',
        'additive', 'compose_rotation', 'compose_scale'
    ]
    for prop in expected_properties:
        assert hasattr(ufbx.AnimLayer, prop), f"AnimLayer missing property: {prop}"


def test_anim_curve_class_has_properties():
    """Test that AnimCurve class has expected properties"""
    expected_properties = [
        'name', 'num_keyframes', 'min_value', 'max_value',
        'min_time', 'max_time'
    ]
    for prop in expected_properties:
        assert hasattr(ufbx.AnimCurve, prop), f"AnimCurve missing property: {prop}"


def test_skin_deformer_class_has_properties():
    """Test that SkinDeformer class has expected properties"""
    expected_properties = ['name', 'clusters']
    for prop in expected_properties:
        assert hasattr(ufbx.SkinDeformer, prop), f"SkinDeformer missing property: {prop}"


def test_skin_cluster_class_has_properties():
    """Test that SkinCluster class has expected properties"""
    expected_properties = ['name', 'num_weights']
    for prop in expected_properties:
        assert hasattr(ufbx.SkinCluster, prop), f"SkinCluster missing property: {prop}"


def test_blend_deformer_class_has_properties():
    """Test that BlendDeformer class has expected properties"""
    expected_properties = ['name', 'channels']
    for prop in expected_properties:
        assert hasattr(ufbx.BlendDeformer, prop), f"BlendDeformer missing property: {prop}"


def test_blend_channel_class_has_properties():
    """Test that BlendChannel class has expected properties"""
    expected_properties = ['name', 'weight']
    for prop in expected_properties:
        assert hasattr(ufbx.BlendChannel, prop), f"BlendChannel missing property: {prop}"


def test_blend_shape_class_has_properties():
    """Test that BlendShape class has expected properties"""
    expected_properties = ['name', 'num_offsets']
    for prop in expected_properties:
        assert hasattr(ufbx.BlendShape, prop), f"BlendShape missing property: {prop}"


def test_constraint_class_has_properties():
    """Test that Constraint class has expected properties"""
    expected_properties = ['name', 'type', 'weight', 'active']
    for prop in expected_properties:
        assert hasattr(ufbx.Constraint, prop), f"Constraint missing property: {prop}"


def test_all_animation_deformer_classes_are_elements():
    """Test that all animation/deformer classes are subclasses of Element"""
    assert issubclass(ufbx.AnimStack, ufbx.Element)
    assert issubclass(ufbx.AnimLayer, ufbx.Element)
    assert issubclass(ufbx.AnimCurve, ufbx.Element)
    assert issubclass(ufbx.SkinDeformer, ufbx.Element)
    assert issubclass(ufbx.SkinCluster, ufbx.Element)
    assert issubclass(ufbx.BlendDeformer, ufbx.Element)
    assert issubclass(ufbx.BlendChannel, ufbx.Element)
    assert issubclass(ufbx.BlendShape, ufbx.Element)
    assert issubclass(ufbx.Constraint, ufbx.Element)


if __name__ == "__main__":
    import sys

    test_functions = [
        test_scene_has_animation_properties,
        test_scene_has_deformer_properties,
        test_anim_stack_class_has_properties,
        test_anim_layer_class_has_properties,
        test_anim_curve_class_has_properties,
        test_skin_deformer_class_has_properties,
        test_skin_cluster_class_has_properties,
        test_blend_deformer_class_has_properties,
        test_blend_channel_class_has_properties,
        test_blend_shape_class_has_properties,
        test_constraint_class_has_properties,
        test_all_animation_deformer_classes_are_elements,
    ]

    failed = 0
    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
        except Exception as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1

    print(f"\n{len(test_functions) - failed}/{len(test_functions)} tests passed")
    sys.exit(0 if failed == 0 else 1)
