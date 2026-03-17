from pgzge.core import GameObject
from tests.pgzge.game_object.test_utilities import TestHandlers


class TestProperties:
    """
    This suite of tests validates the GameObject properties. the tests are all relatively
    simple and cover the basic functionality of the properties.
    """

    def test_name_property(self):
        """
        Tests the name property which is read-only and can only be set in the constructor.
        """
        go = GameObject()
        assert go.name is None

        go = GameObject(name="test")
        assert go.name == "test"

        go = GameObject(name="test.name")
        assert go.name == "test.name"

    def test_active_property(self):
        """
        Tests the active property which is mutable and will trigger the activate and deactivate
        handlers. This does not test propagation of active to children, that is handled in the
        test_parent_and_child.py.
        """
        handlers = TestHandlers()
        go = handlers.create_game_object()

        assert go.active is True
        handlers.validate(activate=go, activate_count=1)

        # Try setting it to true again, nothing should happen
        handlers.reset()
        go.active = True
        assert go.active is True
        handlers.validate()

        handlers.reset()
        go.active = False
        assert go.active is False
        handlers.validate(deactivate=go, deactivate_count=1)

        # Try setting it to false again, nothing should happen
        handlers.reset()
        go.active = False
        assert go.active is False
        handlers.validate()

        # Create a new GameObject, starting deactivated.
        handlers = TestHandlers()
        go = GameObject(
            active=False,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate)
        assert go.active is False
        handlers.validate(deactivate=go, deactivate_count=1)

        handlers.reset()
        go.active = True
        assert go.active is True
        handlers.validate(activate=go, activate_count=1)

    def test_reset(self):
        """
        Validates that reset() works from both the active and inactive states.
        """
        handlers = TestHandlers()
        go = handlers.create_game_object()

        assert go.active is True
        handlers.validate(activate=go, activate_count=1)

        # Now reset, we should get deactivated and then reactivated.
        handlers.reset()
        go.reset()
        assert go.active is True
        handlers.validate(activate=go, activate_count=1, deactivate=go, deactivate_count=1,
                          called_order=["deactivate", "activate"])

        # Now deactivate and reset, we should get deactivated and then activated.
        go.active = False
        handlers.reset()
        go.reset()
        assert go.active is False
        handlers.validate(activate=go, activate_count=1, deactivate=go, deactivate_count=1,
                          called_order=["activate", "deactivate"])

    def test_destroyed(self):
        """
        Validates the destroyed property represents the destroyed state,
        """
        go = GameObject()
        assert not go.is_destroyed

        go.destroy()
        assert go.is_destroyed
        go.destroy()
        assert go.is_destroyed
