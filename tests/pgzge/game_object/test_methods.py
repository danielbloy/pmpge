"""
This suite of tests validates the main GameObject methods. This file focuses on testing a
single GameObject. There are related tests covering hierarchies and subclassing in the
relevant test files.
"""
from tests.pgzge.game_object.test_parent_and_child import parent_three_children
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


def test_destroy_works_on_disabled_object():
    assert False


def test_destroy_works_on_deactivated_object():
    assert False


def test_draw_does_nothing_when_inactive():
    """
    Ensures nothing is done when draw_hierarchy() is called on inactive object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.active = False
    handlers.reset()

    go.draw_hierarchy("surface")

    handlers.validate(called_order=[])


def test_draw_does_nothing_when_invisible():
    """
    Ensures nothing is done when draw_hierarchy() is called on an invisible object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.visible = False
    handlers.reset()

    go.draw_hierarchy("surface")

    handlers.validate(called_order=[])


def test_draw_works_when_disabled():
    """
    Ensures draw_hierarchy() calls handlers on a disabled object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.disabled = True
    handlers.reset()

    go.draw_hierarchy("surface")

    handlers.validate(draw=(go, "surface"), draw_count=1, called_order=["draw"])


def test_updated_removes_destroyed_children():
    """
    Ensures update_hierarchy() removes destroyed children.
    """
    hierarchy = parent_three_children()
    parent = hierarchy.parent
    assert len(parent.go.children) == 3
    hierarchy.find('child-1').go.destroy()
    hierarchy.find('child-3').go.destroy()
    parent.handlers.reset()
    parent.go.update_hierarchy(0.1)
    assert len(parent.go.children) == 1
    parent.handlers.validate(update=(parent.go, 0.1), update_count=1, called_order=["update"])


def test_update_does_nothing_when_inactive():
    """
    Ensures nothing is done when update_hierarchy() is called on an inactive object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.active = False
    handlers.reset()

    go.update_hierarchy(0.1)

    handlers.validate(called_order=[])


def test_update_does_nothing_when_disabled():
    """
    Ensures nothing is done when update_hierarchy() is called on a disabled object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.enabled = False
    handlers.reset()

    go.update_hierarchy(0.1)

    handlers.validate(called_order=[])


def test_update_works_when_invisible():
    """
    Ensures update_hierarchy() calls handlers on an invisible object.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.visible = False
    handlers.reset()

    go.update_hierarchy(0.1)

    handlers.validate(update=(go, 0.1), update_count=1, called_order=["update"])
