import pytest

from pmpge.game_object import GameObject
from pmpge.traits.position import Position


def test_constructor():
    """
    Simple test to ensure that Position works.
    """
    trait = Position(0, 0)
    assert trait.x == 0
    assert trait.y == 0

    trait = Position(10, 20)
    assert trait.x == 10
    assert trait.y == 20

    trait = Position(-1, -2)
    assert trait.x == -1
    assert trait.y == -2


def test_other_properties():
    """
    Validates the position and pos properties work
    """
    # Test the getters first
    trait = Position(0, 0)
    assert trait.x == 0
    assert trait.y == 0

    assert trait.pos == (0, 0)
    assert trait.position == (0, 0)

    trait = Position(10, 20)
    assert trait.x == 10
    assert trait.y == 20

    assert trait.pos == (10, 20)
    assert trait.position == (10, 20)

    trait = Position(-1, -2)
    assert trait.x == -1
    assert trait.y == -2

    assert trait.pos == (-1, -2)
    assert trait.position == (-1, -2)

    # Test the setters
    trait = Position(0, 0)
    trait.pos = (10, 20)

    assert trait.x == 10
    assert trait.y == 20

    assert trait.pos == (10, 20)
    assert trait.position == (10, 20)

    trait.position = (-1, -2)
    assert trait.x == -1
    assert trait.y == -2

    assert trait.pos == (-1, -2)
    assert trait.position == (-1, -2)


# noinspection PyUnresolvedReferences
def test_using_with_game_object():
    """
    Validates it can be used as a GameObject trait (note the pos and position properties
    will not work here.
    """
    go = GameObject(Position(1, 2))
    assert go.x == 1
    assert go.y == 2
    with pytest.raises(AttributeError):
        assert go.pos == (10, 20)

    with pytest.raises(AttributeError):
        assert go.position == (-1, -2)

    assert go.x == 1
    assert go.y == 2

    # Prove that pos does not work.
    go.pos = (10, 20)
    assert go.x == 1
    assert go.y == 2
    assert go.pos == (10, 20)

    with pytest.raises(AttributeError):
        assert go.position == (-1, -2)
