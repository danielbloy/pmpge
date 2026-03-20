"""
This suite of tests validates the main GameObject methods. This file focuses on testing a
single GameObject. There are related tests covering hierarchies and subclassing in the
relevant test files.
"""
from tests.pgzge.game_object.test_utilities import TestHandlers


def test_activate_deactivate_does_nothing_on_destroyed_object():
    """
    Ensures nothing is done when active is changed on a destroyed object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.destroy()
    handlers.reset()

    go.reset()  # Calls activate and deactivate
    go.active = False
    go.active = True
    go.active = False
    go.active = True

    handlers.validate(called_order=[])


def test_draw_does_nothing_on_destroyed_object():
    """
    Ensures nothing is done when draw_hierarchy() is called on a destroyed object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.destroy()
    handlers.reset()

    go.draw_hierarchy("surface")

    handlers.validate(called_order=[])


def test_update_does_nothing_on_destroyed_object():
    """
    Ensures nothing is done when update_hierarchy() is called on a destroyed object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.destroy()
    handlers.reset()

    go.update_hierarchy(0.1)

    handlers.validate(called_order=[])


def test_destroy_does_nothing_on_destroyed_object():
    """
    Ensures nothing is called when active is changed on a destroyed object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.destroy()
    handlers.reset()

    go.destroy()

    handlers.validate(called_order=[])


def test_active_works_on_disabled_object():
    """
    Ensures active works on a disabled object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.enabled = False
    handlers.reset()

    go.active = False
    handlers.validate(deactivate=go, deactivate_count=1, called_order=["deactivate"])

    handlers.reset()
    go.active = True
    handlers.validate(activate=go, activate_count=1, called_order=["activate"])

    handlers.reset()
    go.reset()
    handlers.validate(activate=go, activate_count=1, deactivate=go, deactivate_count=1,
                      called_order=["deactivate", "activate"])

# TODO: Test update_hierarchy on disabled object.
# TODO: Test draw_hierarchy on disabled object.
# TODO: Test destroyed on disabled object.

# TODO: Test impact of active
# TODO: Test impact of enabled
# TODO: Test impact of visible
