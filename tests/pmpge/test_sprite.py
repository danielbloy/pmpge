from pmpge.sprite import Sprite
from tests.pmpge.game_object.test_constructors import validate_properties
from tests.pmpge.test_utilities import Handlers


def test_sprite_constructor():
    """
    Validates the default Sprite constructor with just x and y coordinates.
    """
    sprite = Sprite(0, 0)
    validate_properties(sprite)
    assert sprite.x == 0
    assert sprite.y == 0

    sprite = Sprite(1, 2)
    validate_properties(sprite)
    assert sprite.x == 1
    assert sprite.y == 2

    sprite = Sprite(-1, -7)
    validate_properties(sprite)
    assert sprite.x == -1
    assert sprite.y == -7


def test_pos_and_position_properties_work():
    """
    Validates the position and pos properties work
    """
    # Test the getters first
    sprite = Sprite(0, 0)
    assert sprite.x == 0
    assert sprite.y == 0

    assert sprite.pos == (0, 0)
    assert sprite.position == (0, 0)

    sprite = Sprite(10, 20)
    assert sprite.x == 10
    assert sprite.y == 20

    assert sprite.pos == (10, 20)
    assert sprite.position == (10, 20)

    sprite = Sprite(-1, -2)
    assert sprite.x == -1
    assert sprite.y == -2

    assert sprite.pos == (-1, -2)
    assert sprite.position == (-1, -2)

    # Test the setters
    sprite = Sprite(0, 0)
    sprite.pos = (10, 20)

    assert sprite.x == 10
    assert sprite.y == 20

    assert sprite.pos == (10, 20)
    assert sprite.position == (10, 20)

    sprite.position = (-1, -2)
    assert sprite.x == -1
    assert sprite.y == -2

    assert sprite.pos == (-1, -2)
    assert sprite.position == (-1, -2)


def test_sprite_constructor_with_other_properties():
    """
    Validates the Sprite constructor with some of the other GameObject properties.
    """
    sprite = Sprite(0, 0, name="test")
    validate_properties(sprite, name="test")
    assert sprite.x == 0
    assert sprite.y == 0

    sprite = Sprite(20, -30, name="this-name", enabled=False)
    validate_properties(sprite, name="this-name", enabled=False)
    assert sprite.x == 20
    assert sprite.y == -30


def test_sprite_works_with_handlers():
    """
    Validates that the Sprite works with handlers.
    """
    handlers = Handlers()
    sprite = Sprite(0, 0,
                    activate_handler=handlers.activate,
                    deactivate_handler=handlers.deactivate)

    validate_properties(sprite)
    assert sprite.x == 0
    assert sprite.y == 0
    handlers.validate(activate=sprite, activate_count=1)

    handlers = Handlers()
    sprite = Sprite(10, 20,
                    active=False,
                    activate_handler=handlers.activate,
                    deactivate_handler=handlers.deactivate)

    validate_properties(sprite, active=False)
    assert sprite.x == 10
    assert sprite.y == 20
    handlers.validate(deactivate=sprite, deactivate_count=1)
