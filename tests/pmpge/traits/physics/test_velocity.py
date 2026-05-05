import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = Velocity(0, 0)
    assert trait.vx == 0
    assert trait.vy == 0

    trait = Velocity(10, 20)
    assert trait.vx == 10
    assert trait.vy == 20

    trait = Velocity(-1, -2)
    assert trait.vx == -1
    assert trait.vy == -2

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.x == 0

    with pytest.raises(AttributeError):
        assert trait.y == 0


def test_without_position():
    """
    Validates a Position trait with required.
    """
    go = GameObject(Velocity(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


# noinspection PyUnresolvedReferences
def test_using_with_game_object_positive():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(Position(100, 100), Velocity(10, 20))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 10
    assert go.vy == 20

    # Update with 0 makes no changes
    update_hierarchy(go, 0)
    update_hierarchy(go, 0)
    update_hierarchy(go, 0)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 10
    assert go.vy == 20

    # Update with 1 makes changes
    update_hierarchy(go, 1)
    assert go.x == 110
    assert go.y == 120
    assert go.vx == 10
    assert go.vy == 20

    # Run a few more
    update_hierarchy(go, 1)
    update_hierarchy(go, 1)
    assert go.x == 130
    assert go.y == 160
    assert go.vx == 10
    assert go.vy == 20

    # Run 2 seconds
    update_hierarchy(go, 2)
    assert go.x == 150
    assert go.y == 200
    assert go.vx == 10
    assert go.vy == 20

    # Run a half second
    update_hierarchy(go, 0.5)
    assert go.x == 155
    assert go.y == 210
    assert go.vx == 10
    assert go.vy == 20

    # Change velocity
    go.vx = 1
    go.vy = 2
    update_hierarchy(go, 1)
    assert go.x == 156
    assert go.y == 212
    assert go.vx == 1
    assert go.vy == 2


# noinspection PyUnresolvedReferences
def test_using_with_game_object_negative():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(Position(100, 100), Velocity(-10, -20))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == -10
    assert go.vy == -20

    # Update with 0 makes no changes
    update_hierarchy(go, 0)
    update_hierarchy(go, 0)
    update_hierarchy(go, 0)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == -10
    assert go.vy == -20

    # Update with 1 makes changes
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 80
    assert go.vx == -10
    assert go.vy == -20

    # Run a few more
    update_hierarchy(go, 1)
    update_hierarchy(go, 1)
    assert go.x == 70
    assert go.y == 40
    assert go.vx == -10
    assert go.vy == -20

    # Run 2 seconds
    update_hierarchy(go, 2)
    assert go.x == 50
    assert go.y == 0
    assert go.vx == -10
    assert go.vy == -20

    # Run a half second
    update_hierarchy(go, 0.5)
    assert go.x == 45
    assert go.y == -10
    assert go.vx == -10
    assert go.vy == -20

    # Change velocity
    go.vx = -1
    go.vy = -2
    update_hierarchy(go, 1)
    assert go.x == 44
    assert go.y == -12
    assert go.vx == -1
    assert go.vy == -2
