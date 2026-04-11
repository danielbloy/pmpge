import pytest

from pmpge.game_object import GameObject
from pmpge.traits.physics import Friction
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = Friction(0, 0)
    assert trait.fx == 0
    assert trait.fy == 0

    trait = Friction(10, 20)
    assert trait.fx == 10
    assert trait.fy == 20

    trait = Friction(-1, -2)
    assert trait.fx == -1
    assert trait.fy == -2

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.vx == 0

    with pytest.raises(AttributeError):
        assert trait.vy == 0


def test_without_position():
    """
    Validates a Position trait with required.
    """
    go = GameObject(Velocity(0, 0), Friction(10, 10))
    with pytest.raises(AttributeError):
        go.update_hierarchy(0)


def test_without_velocity():
    """
    Validates a Velocity trait with required.
    """
    go = GameObject(Position(10, 20), Friction(10, 10))
    with pytest.raises(AttributeError):
        go.update_hierarchy(0)


# noinspection PyUnresolvedReferences
def test_using_with_game_object_positive():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(
        Position(1000, 1000),
        Velocity(100, 100),
        Friction(10, 20))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 100
    assert go.vy == 100
    assert go.fx == 10
    assert go.fy == 20

    # Update with 0 makes no changes
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 100
    assert go.vy == 100
    assert go.fx == 10
    assert go.fy == 20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 1100
    assert go.y == 1100
    assert go.vx == 90  # Remember, friction retards velocity
    assert go.vy == 80
    assert go.fx == 10
    assert go.fy == 20

    # Run a few more
    go.update_hierarchy(1)
    go.update_hierarchy(1)
    assert go.x == 1270
    assert go.y == 1240
    assert go.vx == 70
    assert go.vy == 40
    assert go.fx == 10
    assert go.fy == 20

    # Run 2 seconds
    go.update_hierarchy(2)
    assert go.x == 1410
    assert go.y == 1320
    assert go.vx == 50
    assert go.vy == 0
    assert go.fx == 10
    assert go.fy == 20

    # Run a half second
    go.update_hierarchy(0.5)
    assert go.x == 1435
    assert go.y == 1320
    assert go.vx == 45
    assert go.vy == 0  # We do not go below zero with friction
    assert go.fx == 10
    assert go.fy == 20

    # Change friction
    go.fx = 1
    go.fy = 2
    go.update_hierarchy(1)
    assert go.x == 1480
    assert go.y == 1320
    assert go.vx == 44
    assert go.vy == 0
    assert go.fx == 1
    assert go.fy == 2


# noinspection PyUnresolvedReferences
def test_using_with_game_object_negative():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(
        Position(1000, 1000),
        Velocity(100, 100),
        Friction(-10, -20))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 100
    assert go.vy == 100
    assert go.fx == -10
    assert go.fy == -20

    # Update with 0 makes no changes
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 100
    assert go.vy == 100
    assert go.fx == -10
    assert go.fy == -20

    # Run a few more
    go.update_hierarchy(1)
    go.update_hierarchy(1)
    assert go.x == 1210
    assert go.y == 1220
    assert go.vx == 120
    assert go.vy == 140
    assert go.fx == -10
    assert go.fy == -20

    # Run 2 seconds
    go.update_hierarchy(2)
    assert go.x == 1450
    assert go.y == 1500
    assert go.vx == 140
    assert go.vy == 180
    assert go.fx == -10
    assert go.fy == -20

    # Run a half second
    go.update_hierarchy(0.5)
    assert go.x == 1520
    assert go.y == 1590
    assert go.vx == 145
    assert go.vy == 190
    assert go.fx == -10
    assert go.fy == -20

    # Change friction
    go.fx = -1
    go.fy = -2
    go.update_hierarchy(1)
    assert go.x == 1665
    assert go.y == 1780
    assert go.vx == 146
    assert go.vy == 192
    assert go.fx == -1
    assert go.fy == -2


# noinspection PyUnresolvedReferences
def test_trait_order_matters():
    """
    Validates that the order traits are added matters.
    """
    go = GameObject(
        Position(1000, 1000),
        Velocity(100, 100),
        Friction(10, 20))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 100
    assert go.vy == 100
    assert go.fx == 10
    assert go.fy == 20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 1100
    assert go.y == 1100
    assert go.vx == 90  # Remember, friction retards velocity
    assert go.vy == 80
    assert go.fx == 10
    assert go.fy == 20

    # Switch Velocity and Friction
    go = GameObject(
        Position(1000, 1000),
        Friction(10, 20),
        Velocity(100, 100))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 100
    assert go.vy == 100
    assert go.fx == 10
    assert go.fy == 20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 1090
    assert go.y == 1080
    assert go.vx == 90  # Remember, friction retards velocity
    assert go.vy == 80
    assert go.fx == 10
    assert go.fy == 20


# noinspection PyUnresolvedReferences
def test_friction_when_velocity_hits_zero():
    """
    Validates that the friction trait works (by doing nothing) when velocity hits zero.
    """
    go = GameObject(
        Position(1000, 1000),
        Velocity(2, 3),
        Friction(1, 1))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 2
    assert go.vy == 3
    assert go.fx == 1
    assert go.fy == 1

    go.update_hierarchy(1)
    assert go.x == 1002
    assert go.y == 1003
    assert go.vx == 1
    assert go.vy == 2
    assert go.fx == 1
    assert go.fy == 1

    go.update_hierarchy(1)
    assert go.x == 1003
    assert go.y == 1005
    assert go.vx == 0
    assert go.vy == 1
    assert go.fx == 1
    assert go.fy == 1

    go.update_hierarchy(1)
    assert go.x == 1003
    assert go.y == 1006
    assert go.vx == 0
    assert go.vy == 0
    assert go.fx == 1
    assert go.fy == 1

    go.update_hierarchy(1)
    go.update_hierarchy(1)
    go.update_hierarchy(1)
    assert go.x == 1003
    assert go.y == 1006
    assert go.vx == 0
    assert go.vy == 0
    assert go.fx == 1
    assert go.fy == 1

    # Now try with negative friction on velocity, this will increase velocity.
    go = GameObject(
        Position(1000, 1000),
        Velocity(2, 3),
        Friction(-1, -1))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == 2
    assert go.vy == 3
    assert go.fx == -1
    assert go.fy == -1

    go.update_hierarchy(1)
    assert go.x == 1002
    assert go.y == 1003
    assert go.vx == 3
    assert go.vy == 4
    assert go.fx == -1
    assert go.fy == -1

    # Now try with negative friction on negative velocity, this will not change
    # velocity as velocity is negative
    go = GameObject(
        Position(1000, 1000),
        Velocity(-2, -3),
        Friction(-1, -1))
    assert go.x == 1000
    assert go.y == 1000
    assert go.vx == -2
    assert go.vy == -3
    assert go.fx == -1
    assert go.fy == -1

    go.update_hierarchy(1)
    assert go.x == 998
    assert go.y == 997
    assert go.vx == -2
    assert go.vy == -3
    assert go.fx == -1
    assert go.fy == -1
