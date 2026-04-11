import pytest

from pmpge.game_object import GameObject
from pmpge.traits.position import Position, StayInBounds


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = StayInBounds(0, 0, 0, 0)
    assert trait.min_x == 0
    assert trait.min_y == 0
    assert trait.max_x == 0
    assert trait.max_y == 0

    trait = StayInBounds(10, 20, 30, 40)
    assert trait.min_x == 10
    assert trait.min_y == 20
    assert trait.max_x == 30
    assert trait.max_y == 40

    trait = StayInBounds(-1, -2, -3, -4)
    assert trait.min_x == -1
    assert trait.min_y == -2
    assert trait.max_x == -3
    assert trait.max_y == -4

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0


# noinspection PyUnresolvedReferences
def test_using_with_game_object():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(Position(10, 20), StayInBounds(0, 10, 50, 40))
    assert go.x == 10
    assert go.y == 20
    assert go.min_x == 0
    assert go.min_y == 10
    assert go.max_x == 50
    assert go.max_y == 40

    # Inside bounds, nothing changes.
    go.update_hierarchy(0)
    assert go.x == 10
    assert go.y == 20
    assert go.min_x == 0
    assert go.min_y == 10
    assert go.max_x == 50
    assert go.max_y == 40

    # Outside lower x
    go.x = -1
    go.update_hierarchy(0)
    assert go.x == 0
    assert go.y == 20
    assert go.min_x == 0
    assert go.min_y == 10
    assert go.max_x == 50
    assert go.max_y == 40

    # Outside lower y
    go.y = 9
    go.update_hierarchy(0)
    assert go.x == 0
    assert go.y == 10
    assert go.min_x == 0
    assert go.min_y == 10
    assert go.max_x == 50
    assert go.max_y == 40

    # Outside upper x
    go.x = 51
    go.update_hierarchy(0)
    assert go.x == 50
    assert go.y == 10
    assert go.min_x == 0
    assert go.min_y == 10
    assert go.max_x == 50
    assert go.max_y == 40

    # Outside upper y
    go.y = 41
    go.update_hierarchy(0)
    assert go.x == 50
    assert go.y == 40
    assert go.min_x == 0
    assert go.min_y == 10
    assert go.max_x == 50
    assert go.max_y == 40
