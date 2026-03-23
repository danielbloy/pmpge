"""
This suite of tests validates the propagation of state and handlers between
parent and children.
"""
from tests.pgzge.game_object.test_utilities import TestHierarchy


def parent_one_child():
    return (
        TestHierarchy("parent_one_child")
        .add_child("child")
    )


def parent_two_children():
    return (
        TestHierarchy("parent_two_children")
        .add_child("child-1")
        .add_child("child-2")
    )


def parent_three_children():
    return (
        TestHierarchy("parent_two_children")
        .add_child("child-1")
        .add_child("child-2")
        .add_child("child-3")
    )


def parent_one_child_one_grandchild():
    return (
        TestHierarchy("parent_one_child_one_grandchild")
        .add_child("child")
        .add_grandchild("child", "grandchild")
    )


def parent_two_children_one_grandchild():
    return (
        TestHierarchy("parent_two_children_one_grandchild")
        .add_child("child-1")
        .add_grandchild("child-1", "grandchild")
        .add_child("child-2")
    )


def parent_three_children_six_grandchildren():
    return (
        TestHierarchy("parent_three_children_six_grandchildren")
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
    child1.handlers.validate()  # No de-activate event for child1 but should pass through
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
