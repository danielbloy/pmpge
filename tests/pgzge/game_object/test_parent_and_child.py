"""
This suite of tests validates the propagation of state and handlers between
parent and children.
"""
from tests.pgzge.game_object.test_utilities import TestHierarchy


def create_simple_hierarchy():
    """
    Creates a hierarchy of a single parent with two children, no grandchildren.
    """
    hierarchy = TestHierarchy()

    hierarchy.add_child("child-1")
    hierarchy.add_child("child-2")
    hierarchy.reset()
    return hierarchy


def test_active_propagates_to_children():
    """
    Validates that the active state is propagated to children.
    """
    hierarchy = create_simple_hierarchy()
    hierarchy.parent.go.active = False
    hierarchy.validate_properties(active=False)
    hierarchy.validate_called_order(["deactivate"])
    hierarchy.reset()
    hierarchy.parent.go.active = True
    hierarchy.validate_properties(active=True)
    hierarchy.validate_called_order(["activate"])

# TODO: Test all of the more complex parent and child checks.Validate the parent passed in works.
# TODO: Validate that children can override their parents state such as active (but it makes no difference).

# TODO: test propagation of active property to children
# TODO: Ensure handlers are called in the correct order
# TODO: Test reset propagates to children
# TODO: Test destroy propagates to children
# TODO: Test add_child()
# TODO: Test remove_child()
# TODO: Test draw_hierarchy()
# TODO: Test update_hierarchy()
