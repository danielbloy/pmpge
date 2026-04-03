"""
This suite of tests validates the propagation of state and handlers between
parent and children.
"""
import pytest

from pmpge.game_object import GameObject
from tests.pmpge.game_object.test_utilities import Hierarchy


def parent_one_child():
    return (
        Hierarchy("parent_one_child")
        .add_child("child")
    )


def parent_two_children():
    return (
        Hierarchy("parent_two_children")
        .add_child("child-1")
        .add_child("child-2")
    )


def parent_three_children():
    return (
        Hierarchy("parent_two_children")
        .add_child("child-1")
        .add_child("child-2")
        .add_child("child-3")
    )


def parent_one_child_one_grandchild():
    return (
        Hierarchy("parent_one_child_one_grandchild")
        .add_child("child")
        .add_grandchild("child", "grandchild")
    )


def parent_two_children_one_grandchild():
    return (
        Hierarchy("parent_two_children_one_grandchild")
        .add_child("child-1")
        .add_grandchild("child-1", "grandchild")
        .add_child("child-2")
    )


def parent_three_children_six_grandchildren():
    return (
        Hierarchy("parent_three_children_six_grandchildren")
        .add_child("child-1")
        .add_grandchild("child-1", "grandchild-1")
        .add_grandchild("child-1", "grandchild-2")
        .add_grandchild("child-1", "grandchild-3")
        .add_grandchild("child-1", "grandchild-4")
        .add_child("child-2")
        .add_child("child-3")
        .add_grandchild("child-3", "grandchild-5")
        .add_grandchild("child-3", "grandchild-6")

    )


def all_hierarchies():
    """
    Returns a list of all hierarchies to test.
    """
    hierarchies = [
        parent_one_child(),
        parent_two_children(),
        parent_three_children(),
        parent_one_child_one_grandchild(),
        parent_two_children_one_grandchild(),
        parent_three_children_six_grandchildren()
    ]

    for h in hierarchies:
        h.reset()

    return hierarchies


def test_activate_deactivate_propagates_to_children():
    """
    Validates that the active state is propagated to children.
    """

    def test_when_all_active(hierarchy):
        hierarchy.parent.go.active = False
        hierarchy.validate_properties(active=False)
        hierarchy.validate_called_order(["deactivate"])

        # Try deactivating a second time, no events
        hierarchy.reset()
        hierarchy.parent.go.active = False
        hierarchy.validate_properties(active=False)
        hierarchy.validate_called_order([])

        hierarchy.reset()
        hierarchy.parent.go.active = True
        hierarchy.validate_properties(active=True)
        hierarchy.validate_called_order(["activate"])

        # Try activating a second time, no events
        hierarchy.reset()
        hierarchy.parent.go.active = True
        hierarchy.validate_properties(active=True)
        hierarchy.validate_called_order([])

    for h in all_hierarchies():
        test_when_all_active(h)


def test_reset_propagates_to_children():
    """
    Validates that the active state is propagated to children.
    """

    def test_when_all_active(hierarchy):
        hierarchy.parent.go.reset()
        hierarchy.validate_properties(active=True)
        hierarchy.validate_called_order(["deactivate", "activate"])

        # try a second reset, we should get the same again.
        hierarchy.reset()
        hierarchy.parent.go.reset()
        hierarchy.validate_properties(active=True)
        hierarchy.validate_called_order(["deactivate", "activate"])

        # Switch the active state to test the reverse
        hierarchy.parent.go.active = False
        hierarchy.reset()

        hierarchy.parent.go.reset()
        hierarchy.validate_properties(active=False)
        hierarchy.validate_called_order(["activate", "deactivate"])

        # Try a second reset, we should ge the same again.
        hierarchy.reset()
        hierarchy.parent.go.reset()
        hierarchy.validate_properties(active=False)
        hierarchy.validate_called_order(["activate", "deactivate"])

    for h in all_hierarchies():
        test_when_all_active(h)


def test_draw_propagates_to_children():
    """
    Validates that draw is propagated to children all active children.
    """

    def test_when_all_active(hierarchy):
        hierarchy.parent.go.draw_hierarchy("surface")
        hierarchy.validate_called_order(["draw"])

        # Try a second invocation, we should get the same result.
        hierarchy.reset()
        hierarchy.parent.go.draw_hierarchy("surface")
        hierarchy.validate_called_order(["draw"])

    for h in all_hierarchies():
        test_when_all_active(h)


def test_update_propagates_to_children():
    """
    Validates that update is propagated to all active children.
    """

    def test_when_all_active(hierarchy):
        hierarchy.parent.go.update_hierarchy(0.1)
        hierarchy.validate_called_order(["update"])

        # Try a second invocation, we should get the same result.
        hierarchy.reset()
        hierarchy.parent.go.update_hierarchy(0.1)
        hierarchy.validate_called_order(["update"])

    for h in all_hierarchies():
        test_when_all_active(h)


def test_destroy_propagates_to_children():
    """
    Validates that destroy is propagated to all active children.
    """

    def test_when_all_active(hierarchy):
        hierarchy.parent.go.destroy()
        hierarchy.validate_properties(active=False, alive=False)
        hierarchy.validate_called_order(
            ["deactivate", "destroy"], reverse=True, interlace=True)

        # Try again, this time there should be no events.
        hierarchy.reset()
        hierarchy.parent.go.destroy()
        hierarchy.validate_properties(active=False, alive=False)
        hierarchy.validate_called_order([])

    for h in all_hierarchies():
        test_when_all_active(h)


def test_activated_deactivated_propagated_through_disabled_objects():
    """
    Ensures activated() and deactivated() are called on a disabled object.
    """
    hierarchy = parent_three_children_six_grandchildren()
    hierarchy.find('child-3').go.enabled = False
    hierarchy.find('grandchild-5').go.enabled = False

    hierarchy.reset()
    hierarchy.parent.go.active = False
    hierarchy.validate_properties(active=False)
    hierarchy.validate_called_order(["deactivate"])

    hierarchy.reset()
    hierarchy.parent.go.active = True
    hierarchy.validate_properties(active=True)
    hierarchy.validate_called_order(["activate"])

    hierarchy.reset()
    hierarchy.parent.go.reset()
    hierarchy.validate_properties(active=True)
    hierarchy.validate_called_order(["deactivate", "activate"])


def test_activated_deactivated_propagated_through_inactive_objects():
    """
    Ensures activated() and deactivated() are propagated through disabled objects.
    """
    hierarchy = parent_two_children_one_grandchild()
    hierarchy.find(
        'child-1').go.active = False  # This will disable grandchild-5 and 6 so we re-enable one
    hierarchy.find('grandchild').go.active = True

    hierarchy.reset()
    hierarchy.parent.go.active = False
    hierarchy.validate_properties(active=False)

    parent = hierarchy.parent
    child1 = hierarchy.find('child-1')
    child2 = hierarchy.find('child-2')
    grandchild = hierarchy.find('grandchild')

    parent.handlers.validate(deactivate=parent.go, deactivate_count=1)
    child1.handlers.validate()  # No deactivate event for child1 but should pass through
    grandchild.handlers.validate(deactivate=grandchild.go, deactivate_count=1)
    child2.handlers.validate(deactivate=child2.go, deactivate_count=1)


def test_enabled_disabled_does_not_propagate():
    """
    Ensures enabled and disabled does not propagate to children.
    """
    hierarchy = parent_one_child_one_grandchild()
    parent = hierarchy.parent
    child = hierarchy.find('child')
    grandchild = hierarchy.find('grandchild')

    parent.go.enabled = False
    assert child.go.enabled == True
    assert grandchild.go.enabled == True

    parent.go.disabled = False
    assert child.go.enabled == True
    assert grandchild.go.enabled == True

    parent.go.disabled = True
    assert child.go.enabled == True
    assert grandchild.go.enabled == True

    parent.go.enabled = True
    assert child.go.enabled == True
    assert grandchild.go.enabled == True


def test_destroy_works_on_disabled_object():
    """
    Ensures destroy works on disabled objects.
    """

    def test_when_disabled(hierarchy):
        # Disable the parent and first child if one exists.
        hierarchy.parent.go.enabled = False
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.enabled = False

        hierarchy.parent.go.destroy()
        hierarchy.validate_called_order(["deactivate", "destroy"], reverse=True, interlace=True)

    for h in all_hierarchies():
        test_when_disabled(h)


def test_destroy_works_on_deactivated_object():
    """
    Ensures destroy works on deactivated objects.
    """

    def test_when_deactivated(hierarchy):
        # Deactivate the parent (this deactivates the entire hierarchy)
        hierarchy.parent.go.active = False
        hierarchy.reset()

        hierarchy.parent.go.destroy()
        hierarchy.validate_properties(active=False, alive=False)
        hierarchy.validate_called_order(["destroy"], reverse=True)

    for h in all_hierarchies():
        test_when_deactivated(h)


def test_draw_does_nothing_when_inactive():
    """
    Ensures draw_hierarchy() does nothing on inactive objects. It should also not propagate.
    """

    def test_when_inactive(hierarchy):
        # Deactivate the parent (this deactivates the entire hierarchy)
        hierarchy.parent.go.active = False
        # Reactivate all grandchildren and first child
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.active = True
        for grandchild in hierarchy.grandchildren:
            grandchild.go.active = True
        hierarchy.reset()

        hierarchy.parent.go.draw_hierarchy("surface")
        hierarchy.validate_called_order([])

    for h in all_hierarchies():
        test_when_inactive(h)


def test_draw_does_nothing_when_invisible():
    """
    Ensures draw_hierarchy() does nothing on invisible objects. The visible property only
    applies to the object itself so the update still propagates
    """

    def test_when_invisible(hierarchy):
        invisible = [hierarchy.parent.go]

        # Hide the parent and first child if one exists.
        hierarchy.parent.go.visible = False
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.visible = False
            invisible.append(hierarchy.children[0].go)

        hierarchy.parent.go.draw_hierarchy("surface")
        hierarchy.validate_called_order(["draw"], exclude=invisible)

    for h in all_hierarchies():
        test_when_invisible(h)


def test_draw_works_when_disabled():
    """
    Ensures draw_hierarchy() works as normal on disabled objects as disabled/enabled only
    applies to update_hierarchy().
    """

    def test_when_disabled(hierarchy):

        # Disable the parent and first child if one exists.
        hierarchy.parent.go.enabled = False
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.enabled = False

        hierarchy.parent.go.draw_hierarchy("surface")
        hierarchy.validate_called_order(["draw"])

    for h in all_hierarchies():
        test_when_disabled(h)


def test_updated_removes_destroyed_children():
    """
    Validates that update_hierarchy() removes destroyed children.
    """
    hierarchy = parent_three_children_six_grandchildren()
    parent = hierarchy.parent
    assert len(parent.go.children) == 3
    hierarchy.find('child-1').go.destroy()
    hierarchy.find('child-3').go.destroy()
    hierarchy.reset()

    parent.go.update_hierarchy(0.1)

    assert len(parent.go.children) == 1
    parent.handlers.validate(update=(parent.go, 0.1), update_count=1, called_order=["update"])
    child2 = hierarchy.find('child-2')
    child2.handlers.validate(update=(child2.go, 0.1), update_count=1, called_order=["update"])

    # The destroyed children should get no events
    hierarchy.find('child-1').handlers.validate([])
    hierarchy.find('child-3').handlers.validate([])


def test_update_does_nothing_when_inactive():
    """
    Ensures update_hierarchy() does nothing on inactive objects. It should also not propagate.
    """

    def test_when_inactive(hierarchy):
        # Deactivate the parent (this deactivates the entire hierarchy)
        hierarchy.parent.go.active = False
        # Reactivate all grandchildren and first child
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.active = True
        for grandchild in hierarchy.grandchildren:
            grandchild.go.active = True
        hierarchy.reset()

        hierarchy.parent.go.update_hierarchy(0.1)
        hierarchy.validate_called_order([])

    for h in all_hierarchies():
        test_when_inactive(h)


def test_update_does_nothing_when_disabled():
    """
    Ensures update_hierarchy() does nothing on disabled objects. The enabled property only
    applies to the object itself so the update still propagates
    """

    def test_when_disabled(hierarchy):
        disabled = [hierarchy.parent.go]

        # Disable the parent and first child if one exists.
        hierarchy.parent.go.enabled = False
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.enabled = False
            disabled.append(hierarchy.children[0].go)

        hierarchy.parent.go.update_hierarchy(0.1)
        hierarchy.validate_called_order(["update"], exclude=disabled)

    for h in all_hierarchies():
        test_when_disabled(h)


def test_update_works_when_invisible():
    """
    Ensures update_hierarchy() works as normal on invisible objects as visible only
    applies to draw_hierarchy().
    """

    def test_when_disabled(hierarchy):

        # Hide the parent and first child if one exists.
        hierarchy.parent.go.visible = False
        if len(hierarchy.children) > 0:
            hierarchy.children[0].go.visible = False

        hierarchy.parent.go.update_hierarchy(0.1)
        hierarchy.validate_called_order(["update"])

    for h in all_hierarchies():
        test_when_disabled(h)


def test_add_child():
    """
    Validates that a child can be added to a parent.
    """
    parent = GameObject()
    child = GameObject()

    assert len(parent.children) == 0
    assert child.parent is None

    # Add none, this should not error
    # noinspection PyTypeChecker
    parent.add_child(None)
    assert len(parent.children) == 0

    # Add child
    parent.add_child(child)
    assert len(parent.children) == 1
    assert child.parent == parent

    # Add a second time, this should not error.
    parent.add_child(child)
    assert len(parent.children) == 1
    assert child.parent == parent


def test_add_child_to_another_parent():
    """
    Validates that a child cannot be added to another parent.
    """
    parent1 = GameObject()
    parent2 = GameObject()
    child = GameObject(parent=parent1)

    assert len(parent1.children) == 1
    assert len(parent2.children) == 0
    assert child.parent is parent1

    with pytest.raises(ValueError):
        parent2.add_child(child)

    assert len(parent1.children) == 1
    assert len(parent2.children) == 0
    assert child.parent is parent1


def test_remove_child():
    """
    Validates that a child can be removed from a parent.
    """
    parent = GameObject()
    child1 = GameObject(parent=parent)
    child2 = GameObject(parent=parent)
    child3 = GameObject(parent=parent)

    assert len(parent.children) == 3
    assert child1.parent is parent
    assert child2.parent is parent
    assert child3.parent is parent

    # Remove none, this should not error
    # noinspection PyTypeChecker
    parent.remove_child(None)
    assert len(parent.children) == 3
    assert child1.parent is parent
    assert child2.parent is parent
    assert child3.parent is parent

    # Remove child
    parent.remove_child(child2)
    assert len(parent.children) == 2
    assert child1.parent == parent
    assert child2.parent is None
    assert child3.parent == parent

    # Remove a second time, this should not error.
    parent.remove_child(child1)
    assert len(parent.children) == 1
    assert child1.parent is None
    assert child2.parent is None
    assert child3.parent == parent

    # Remove a second child


def test_remove_child_from_another_parent():
    """
    Validates that a child cannot be removed from another parent.
    """
    parent1 = GameObject()
    parent2 = GameObject()
    child = GameObject(parent=parent1)

    assert len(parent1.children) == 1
    assert len(parent2.children) == 0
    assert child.parent is parent1

    with pytest.raises(ValueError):
        parent2.remove_child(child)

    assert len(parent1.children) == 1
    assert len(parent2.children) == 0
    assert child.parent is parent1
