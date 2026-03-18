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


# TODO: Add more complex scenarios such as grandchildren.


def all_hierarchies():
    """
    Returns a list of all hierarchies to test.
    """
    hierarchies = [
        parent_one_child(),
        parent_two_children(),
        parent_three_children(),
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
        hierarchy.reset()
        hierarchy.parent.go.active = True
        hierarchy.validate_properties(active=True)
        hierarchy.validate_called_order(["activate"])

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

        hierarchy.parent.go.active = False
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

    for h in all_hierarchies():
        test_when_all_active(h)


def test_update_propagates_to_children():
    """
    Validates that update is propagated to all active children.
    """

    def test_when_all_active(hierarchy):
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
        hierarchy.validate_properties(alive=False)
        hierarchy.validate_called_order(["deactivate", "destroy"])

    for h in all_hierarchies():
        test_when_all_active(h)

# TODO: Test when only some children are active/enabled.


# TODO: Test all of the more complex parent and child checks.Validate the parent passed in works.
# TODO: Validate that children can override their parents state such as active (but it makes no difference).

# TODO: Test draw/update only when visible, enabled/active.

# TODO: Test add_child()
# TODO: Test remove_child()
# TODO: Test draw_hierarchy()
# TODO: Test update_hierarchy()
