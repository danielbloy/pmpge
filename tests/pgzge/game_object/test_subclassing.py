from pgzge.core import GameObject
from tests.pgzge.game_object.test_utilities import TestHandlers


class GameObjectSubclass(GameObject):
    """
    Subclass GameObject and override all the supported methods.
    """

    def activated(self) -> None:
        self.handlers.activate(self)

    def deactivated(self) -> None:
        self.handlers.deactivate(self)

    def draw(self, surface):
        self.handlers.draw(self, surface)

    def update(self, dt) -> None:
        self.handlers.update(self, dt)

    def destroyed(self) -> None:
        self.handlers.destroy(self)

    @property
    def handlers(self) -> TestHandlers:
        if not hasattr(self, '_handlers'):
            self._handlers = TestHandlers()

        return self._handlers


class TestSubclassing:
    """
    This suite of tests validates that the main overridable placeholder methods are
    called at the expected points.
    """

    def test_activated_in_constructor(self):
        """
        Validates that activated is called during construction.
        """
        go = GameObjectSubclass()
        go.handlers.validate(activate=go, activate_count=1)

    def test_deactivated_in_constructor(self):
        """
        Validates that deactivated is called during construction.
        """
        go = GameObjectSubclass()
        go.handlers.validate(activate=go, activate_count=1)

    def test_draw_handler_called(self):
        """
        This is a basic test that ensures the draw handler is called.
        """
        go = GameObjectSubclass()

        go.handlers.validate(activate=go, activate_count=1)
        go.handlers.reset()

        go.draw_hierarchy("surface")
        go.handlers.validate(draw=(go, "surface"), draw_count=1)

    def test_update_handler_called(self):
        """
        This is a basic test that ensures the update handler is called.
        """
        go = GameObjectSubclass()

        go.handlers.validate(activate=go, activate_count=1)
        go.handlers.reset()

        go.update_hierarchy(0.1)
        go.handlers.validate(update=(go, 0.1), update_count=1)

    def test_destroy_handler_called(self):
        """
        This is a basic test that ensures the destroy handler is called.
        """
        go = GameObjectSubclass()
        go.handlers.validate(activate=go, activate_count=1)
        go.handlers.reset()

        go.destroy()  # This will also deactivate the GameObject
        go.handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1,
                             called_order=["deactivate", "destroy"])

    def test_activate_draw_update_deactivate_destroyed_handlers_called(self):
        """
        This is a basic test that ensures all the handlers are called.
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
