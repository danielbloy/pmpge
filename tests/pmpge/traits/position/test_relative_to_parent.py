import pytest

from pmpge.game_object import GameObject
from pmpge.traits.position import Position, RelativeToParent


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = RelativeToParent(0, 0)
    assert trait.offset_x == 0
    assert trait.offset_y == 0

    trait = RelativeToParent(10, 20)
    assert trait.offset_x == 10
    assert trait.offset_y == 20

    trait = RelativeToParent(-1, -2)
    assert trait.offset_x == -1
    assert trait.offset_y == -2

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0


# noinspection PyUnresolvedReferences
def test_works_without_position_trait():
    """
    Validates that a RelativeToParent trait can be used without being combined
    with a Position trait as it implicitly creates the x and y properties.
    """
    go = GameObject(RelativeToParent(1, 2))
    assert go.offset_x == 1
    assert go.offset_y == 2

    with pytest.raises(AttributeError):
        assert go.x == 0

    with pytest.raises(AttributeError):
        assert go.y == 0

    go.update_hierarchy(0)
    assert go.x == 1
    assert go.y == 2
    assert go.offset_x == 1
    assert go.offset_y == 2

    go.update_hierarchy(1)
    assert go.x == 1
    assert go.y == 2
    assert go.offset_x == 1
    assert go.offset_y == 2


# noinspection PyUnresolvedReferences
def test_works_without_parent():
    """
    Validates that the position of the GameObject is updated relative to (0, 0) if there
    is no parent object.
    """
    go = GameObject(Position(10, 20), RelativeToParent(1, 2))
    assert go.x == 10
    assert go.y == 20
    assert go.offset_x == 1
    assert go.offset_y == 2

    go.update_hierarchy(0)
    assert go.x == 1
    assert go.y == 2
    assert go.offset_x == 1
    assert go.offset_y == 2

    go.offset_x = -13
    go.offset_y = 17

    go.update_hierarchy(1)
    assert go.x == -13
    assert go.y == 17
    assert go.offset_x == -13
    assert go.offset_y == 17

    # run the update loads of times and there should be no change to the value.
    go.update_hierarchy(0)
    go.update_hierarchy(0.1)
    go.update_hierarchy(2)
    go.update_hierarchy(6)
    go.update_hierarchy(5)
    go.update_hierarchy(1)
    go.update_hierarchy(0.01)
    assert go.x == -13
    assert go.y == 17
    assert go.offset_x == -13
    assert go.offset_y == 17
