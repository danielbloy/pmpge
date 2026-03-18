from pgzge.core import GameObject
from tests.pgzge.game_object.test_utilities import TestHandlers

"""
This suite of tests validate that event handlers can be added and removed.
"""


# noinspection PyTypeChecker
def test_removing_none_when_no_handlers():
    """
    Simple checks to just make sure there are no errors.
    """
    go = GameObject()
    go.remove_draw_handler(None)
    go.remove_update_handler(None)
    go.remove_activate_handler(None)
    go.remove_deactivate_handler(None)
    go.remove_destroy_handler(None)


def test_removing_when_no_handlers():
    """
    Straight forward checks to make sure there are no errors.
    """
    handlers = TestHandlers()
    go = GameObject()
    go.remove_draw_handler(handlers.draw)
    go.remove_update_handler(handlers.update)
    go.remove_activate_handler(handlers.activate)
    go.remove_deactivate_handler(handlers.deactivate)
    go.remove_destroy_handler(handlers.destroy)

    go.draw("none")
    go.update(0.0)
    go.deactivate()
    go.activate()
    go.destroy()
    handlers.validate()


# noinspection PyTypeChecker
def test_adding_non_when_no_handlers():
    """
    Simple checks to just make sure there are no errors.
    """
    go = GameObject()
    go.add_draw_handler(None)
    go.add_update_handler(None)
    go.add_activate_handler(None)
    go.add_deactivate_handler(None)
    go.add_destroy_handler(None)


def test_adding_single_handler():
    """
    Validates that we can add a single handler to empty lists.
    """
    handlers = TestHandlers()
    go = GameObject()
    go.add_draw_handler(handlers.draw)
    go.draw_hierarchy("none")
    handlers.validate(draw=(go, "none"), draw_count=1, called_order=["draw"])

    handlers.reset()
    go = GameObject()
    go.add_update_handler(handlers.update)
    go.update_hierarchy(1.0)
    handlers.validate(update=(go, 1.0), update_count=1, called_order=["update"])
    handlers.reset()

    handlers.reset()
    go = GameObject(active=False)
    go.add_activate_handler(handlers.activate)
    go.activate()
    handlers.validate(activate=go, activate_count=1, called_order=["activate"])
    handlers.reset()

    handlers.reset()
    go = GameObject()
    go.add_deactivate_handler(handlers.deactivate)
    go.deactivate()
    handlers.validate(deactivate=go, deactivate_count=1, called_order=["deactivate"])

    handlers.reset()
    go = GameObject()
    go.add_destroy_handler(handlers.destroy)
    go.destroy()
    handlers.validate(destroy=go, destroy_count=1, called_order=["destroy"])


def test_adding_all_single_handler():
    """
    Validates that we can add a single handler to all empty handler lists.
    """

    # Try adding all of them.
    handlers = TestHandlers()
    go = GameObject()
    go.add_draw_handler(handlers.draw)
    go.add_update_handler(handlers.update)
    go.add_activate_handler(handlers.activate)
    go.add_deactivate_handler(handlers.deactivate)
    go.add_destroy_handler(handlers.destroy)

    go.draw_hierarchy("none")
    handlers.validate(draw=(go, "none"), draw_count=1, called_order=["draw"])

    handlers.reset()
    go.update_hierarchy(0.0)
    handlers.validate(update=(go, 0.0), update_count=1, called_order=["update"])

    handlers.reset()
    go.deactivate()
    handlers.validate(deactivate=go, deactivate_count=1, called_order=["deactivate"])

    handlers.reset()
    go.activate()
    handlers.validate(activate=go, activate_count=1, called_order=["activate"])

    handlers.reset()
    go.destroy()
    handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1,
                      called_order=["deactivate", "destroy"])


def test_adding_and_remove_single_handler():
    """
    Validates that we can add a single handler to empty lists.
    """
    handlers = TestHandlers()
    go = GameObject()
    go.add_draw_handler(handlers.draw)
    go.remove_draw_handler(handlers.draw)
    go.draw_hierarchy("none")
    handlers.validate()

    handlers.reset()
    go = GameObject()
    go.add_update_handler(handlers.update)
    go.remove_update_handler(handlers.update)
    go.update_hierarchy(1.0)
    handlers.validate()
    handlers.reset()

    handlers.reset()
    go = GameObject(active=False)
    go.add_activate_handler(handlers.activate)
    go.remove_activate_handler(handlers.activate)
    go.activate()
    handlers.validate()
    handlers.reset()

    handlers.reset()
    go = GameObject()
    go.add_deactivate_handler(handlers.deactivate)
    go.remove_deactivate_handler(handlers.deactivate)
    go.deactivate()
    handlers.validate()

    handlers.reset()
    go = GameObject()
    go.add_destroy_handler(handlers.destroy)
    go.remove_destroy_handler(handlers.destroy)
    go.destroy()
    handlers.validate()


def test_adding_single_handler_twice():
    """
    Validates that we can add a single handler twice to empty lists.
    """
    handlers = TestHandlers()
    go = GameObject()
    go.add_draw_handler(handlers.draw)
    go.add_draw_handler(handlers.draw)
    go.draw_hierarchy("none")
    handlers.validate(draw=(go, "none"), draw_count=2, called_order=["draw", "draw"])

    handlers.reset()
    go = GameObject()
    go.add_update_handler(handlers.update)
    go.add_update_handler(handlers.update)
    go.update_hierarchy(1.0)
    handlers.validate(update=(go, 1.0), update_count=2, called_order=["update", "update"])
    handlers.reset()

    handlers.reset()
    go = GameObject(active=False)
    go.add_activate_handler(handlers.activate)
    go.add_activate_handler(handlers.activate)
    go.activate()
    handlers.validate(activate=go, activate_count=2, called_order=["activate", "activate"])
    handlers.reset()

    handlers.reset()
    go = GameObject()
    go.add_deactivate_handler(handlers.deactivate)
    go.add_deactivate_handler(handlers.deactivate)
    go.deactivate()
    handlers.validate(deactivate=go, deactivate_count=2,
                      called_order=["deactivate", "deactivate"])

    handlers.reset()
    go = GameObject()
    go.add_destroy_handler(handlers.destroy)
    go.add_destroy_handler(handlers.destroy)
    go.destroy()
    handlers.validate(destroy=go, destroy_count=2, called_order=["destroy", "destroy"])


def test_adding_handlers_when_added_through_construction():
    """
    Validates that we can add handlers when some already added through the construction.
    """
    handlers = TestHandlers()

    go = handlers.create_game_object()
    go.add_draw_handler(handlers.draw)
    go.add_update_handler(handlers.update)
    go.add_activate_handler(handlers.activate)
    go.add_deactivate_handler(handlers.deactivate)
    go.add_destroy_handler(handlers.destroy)
    handlers.reset()

    go.draw_hierarchy("none")
    handlers.validate(draw=(go, "none"), draw_count=2, called_order=["draw", "draw"])

    handlers.reset()
    go.update_hierarchy(0.0)
    handlers.validate(update=(go, 0.0), update_count=2, called_order=["update", "update"])

    handlers.reset()
    go.deactivate()
    handlers.validate(deactivate=go, deactivate_count=2,
                      called_order=["deactivate", "deactivate"])

    handlers.reset()
    go.activate()
    handlers.validate(activate=go, activate_count=2, called_order=["activate", "activate"])

    handlers.reset()
    go.destroy()
    handlers.validate(deactivate=go, deactivate_count=2, destroy=go, destroy_count=2,
                      called_order=["deactivate", "deactivate", "destroy", "destroy"])


def test_remove_handlers_when_added_through_construction():
    """
    Validates that we can remove handlers when added through the construction.
    """
    handlers = TestHandlers()
    go = handlers.create_game_object()
    go.remove_draw_handler(handlers.draw)
    go.remove_update_handler(handlers.update)
    go.remove_activate_handler(handlers.activate)
    go.remove_deactivate_handler(handlers.deactivate)
    go.remove_destroy_handler(handlers.destroy)
    handlers.reset()

    go.draw_hierarchy("none")
    handlers.validate()

    handlers.reset()
    go.update_hierarchy(0.0)
    handlers.validate()

    handlers.reset()
    go.deactivate()
    handlers.validate()

    handlers.reset()
    go.activate()
    handlers.validate()

    handlers.reset()
    go.destroy()
    handlers.validate()
