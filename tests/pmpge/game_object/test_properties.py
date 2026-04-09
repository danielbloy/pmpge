"""
This suite of tests validates the GameObject properties. the tests are all relatively
simple and cover the basic functionality of the properties.
"""
from pmpge.game_object import GameObject
from tests.pmpge.test_utilities import Handlers


def test_name_property():
    """
    Tests the name property which is read-only and can only be set in the constructor.
    """
    go = GameObject()
    assert go.name is None

    go = GameObject(name="test")
    assert go.name == "test"

    go = GameObject(name="test.name")
    assert go.name == "test.name"


def test_active_property():
    """
    Tests the active property which is mutable and will trigger the activate and deactivate
    handlers. This does not test propagation of active to children, that is handled in the
    test_parent_and_child.py.
    """
    handlers = Handlers()
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
    handlers = Handlers()
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


def test_reset():
    """
    Validates that reset() works from both the active and inactive states.
    """
    handlers = Handlers()
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


def test_enabled_disabled():
    """
    Enabled is simply a boolean property. Disabled is simply the opposite of enabled and
    provided as a convenience property. It does not propagate or affect children.
    """
    handlers = Handlers()
    go = handlers.create_game_object()
    handlers.reset()

    assert go.enabled is True
    assert go.disabled is False
    handlers.validate()

    go.enabled = False
    assert go.enabled is False
    assert go.disabled is True
    handlers.validate()

    go.disabled = False
    assert go.enabled is True
    assert go.disabled is False
    handlers.validate()

    go.disabled = True
    assert go.enabled is False
    assert go.disabled is True
    handlers.validate()


def test_destroyed():
    """
    Validates the alive property represents the destroyed state,
    """
    go = GameObject()
    assert go.alive

    go.destroy()
    assert not go.alive
    go.destroy()
    assert not go.alive
