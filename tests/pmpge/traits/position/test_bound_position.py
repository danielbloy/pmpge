import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.traits.position import Position, BoundPosition


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = BoundPosition(0, 0, 0, 0)
    assert trait.bounds_position == (0, 0, 0, 0)

    trait = BoundPosition(10, 20, 30, 40)
    assert trait.bounds_position == (10, 20, 30, 40)

    trait = BoundPosition(-1, -2, -3, -4)
    assert trait.bounds_position == (-1, -2, -3, -4)

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
    go = GameObject(Position(10, 20), BoundPosition(0, 10, 50, 40))
    assert go.x == 10
    assert go.y == 20
    assert go.bounds_position == (0, 10, 50, 40)

    # Inside bounds, nothing changes.
    update_hierarchy(go, 0)
    assert go.x == 10
    assert go.y == 20
    assert go.bounds_position == (0, 10, 50, 40)

    # Outside lower x
    go.x = -1
    update_hierarchy(go, 0)
    assert go.x == 0
    assert go.y == 20
    assert go.bounds_position == (0, 10, 50, 40)

    # Outside lower y
    go.y = 9
    update_hierarchy(go, 0)
    assert go.x == 0
    assert go.y == 10
    assert go.bounds_position == (0, 10, 50, 40)

    # Outside upper x
    go.x = 51
    update_hierarchy(go, 0)
    assert go.x == 50
    assert go.y == 10
    assert go.bounds_position == (0, 10, 50, 40)

    # Outside upper y
    go.y = 41
    update_hierarchy(go, 0)
    assert go.x == 50
    assert go.y == 40
    assert go.bounds_position == (0, 10, 50, 40)
