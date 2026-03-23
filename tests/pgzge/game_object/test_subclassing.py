"""
This suite of tests validates that the main overridable placeholder methods are
called at the expected points.
"""
from tests.pgzge.game_object.test_utilities import GameObjectSubclass


def test_activated_in_constructor():
    """
    Validates that activated is called during construction.
    """
    go = GameObjectSubclass()
    go.handlers.validate(activate=go, activate_count=1)


def test_activated_called_before_handler():
    """
    Makes sure that the activated() method is called before activated handlers.
    """
    go = GameObjectSubclass()
    go.deactivate()
    go.handlers.reset()
    go.add_activate_handler(lambda obj: go.handlers.called_order.append("activate_handler"))
    go.activate()
    go.handlers.validate(activate=go, activate_count=1,
                         called_order=["activate", "activate_handler"])


def test_deactivated_in_constructor():
    """
    Validates that deactivated() is called during construction.
    """
    go = GameObjectSubclass()
    go.handlers.validate(activate=go, activate_count=1)


def test_deactivated_called_before_handler():
    """
    Makes sure that the deactivated() method is called before deactivated handlers.
    """
    go = GameObjectSubclass()
    go.add_deactivate_handler(lambda obj: go.handlers.called_order.append("deactivate_handler"))
    go.handlers.reset()
    go.deactivate()
    go.handlers.validate(deactivate=go, deactivate_count=1,
                         called_order=["deactivate", "deactivate_handler"])


def test_draw_called():
    """
    This is a basic test that ensures the draw() method is called.
    """
    go = GameObjectSubclass()

    go.handlers.validate(activate=go, activate_count=1)
    go.handlers.reset()

    go.draw_hierarchy("surface")
    go.handlers.validate(draw=(go, "surface"), draw_count=1)


def test_draw_called_before_draw_handler():
    """
    Makes sure that the draw() method is called before draw handlers.
    """
    go = GameObjectSubclass()

    go.handlers.validate(activate=go, activate_count=1)
    go.add_draw_handler(lambda obj, surface: go.handlers.called_order.append("draw_handler"))
    go.handlers.reset()

    go.draw_hierarchy("surface")
    go.handlers.validate(draw=(go, "surface"), draw_count=1, called_order=["draw", "draw_handler"])


def test_update_called():
    """
    This is a basic test that ensures the update() method is called.
    """

    go = GameObjectSubclass()

    go.handlers.validate(activate=go, activate_count=1)
    go.handlers.reset()

    go.update_hierarchy(0.1)
    go.handlers.validate(update=(go, 0.1), update_count=1)


def test_update_called_before_update_handler_called():
    """
    Makes sure that the update() method is called before update handlers.
    """
    go = GameObjectSubclass()

    go.handlers.validate(activate=go, activate_count=1)
    go.add_update_handler(lambda obj, surface: go.handlers.called_order.append("update_handler"))
    go.handlers.reset()

    go.update_hierarchy(0.1)
    go.handlers.validate(update=(go, 0.1), update_count=1,
                         called_order=["update", "update_handler"])


def test_destroy_called():
    """
    This is a basic test that ensures the destroyed() method is called.
    """
    go = GameObjectSubclass()
    go.handlers.validate(activate=go, activate_count=1)
    go.handlers.reset()

    go.destroy()  # This will also deactivate the GameObject
    go.handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1,
                         called_order=["deactivate", "destroy"])


def test_destroy_called_before_destroy_handler():
    """
    Makes sure that the destroyed() method is called before destroy handlers.
    """
    go = GameObjectSubclass()
    go.handlers.validate(activate=go, activate_count=1)
    go.add_deactivate_handler(lambda obj: go.handlers.called_order.append("deactivate_handler"))
    go.add_destroy_handler(lambda obj: go.handlers.called_order.append("destroy_handler"))
    go.handlers.reset()

    go.destroy()  # This will also deactivate the GameObject
    go.handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1,
                         called_order=["deactivate", "deactivate_handler", "destroy",
                                       "destroy_handler"])


def test_activate_draw_update_deactivate_destroyed_handlers_called():
    """
    This is a basic test that ensures all the methods are called.
    """
    go = GameObjectSubclass()

    go.handlers.validate(activate=go, activate_count=1)

    go.handlers.reset()
    go.draw_hierarchy("surface")
    go.handlers.validate(draw=(go, "surface"), draw_count=1)

    go.handlers.reset()
    go.update_hierarchy(0.1)
    go.handlers.validate(update=(go, 0.1), update_count=1)

    go.handlers.reset()
    go.destroy()  # This will also deactivate the GameObject
    go.handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1,
                         called_order=["deactivate", "destroy"])


def test_methods_not_called_when_destroyed():
    """
    Ensures no the methods are called on a destroyed object.
    """
    go = GameObjectSubclass()
    go.destroy()
    go.handlers.reset()

    go.reset()
    go.draw_hierarchy("surface")
    go.update_hierarchy(0.1)
    go.destroy()

    go.handlers.validate(called_order=[])


def test_activated_deactivated_called_on_disabled_object():
    """
    Ensures activated() and deactivated() are called on a disabled object.
    """
    go = GameObjectSubclass()
    go.enabled = False
    go.handlers.reset()

    go.active = False
    go.handlers.validate(deactivate=go, deactivate_count=1, called_order=["deactivate"])

    go.handlers.reset()
    go.active = True
    go.handlers.validate(activate=go, activate_count=1, called_order=["activate"])

    go.handlers.reset()
    go.reset()
    go.handlers.validate(activate=go, activate_count=1, deactivate=go, deactivate_count=1,
                         called_order=["deactivate", "activate"])
