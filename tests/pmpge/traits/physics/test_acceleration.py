import pytest

from pmpge.game_object import GameObject
from pmpge.traits.physics import Acceleration, Friction, Velocity
from pmpge.traits.position import Position


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = Acceleration(0, 0)
    assert trait.ax == 0
    assert trait.ay == 0

    trait = Acceleration(10, 20)
    assert trait.ax == 10
    assert trait.ay == 20

    trait = Acceleration(-1, -2)
    assert trait.ax == -1
    assert trait.ay == -2

    # At this point there will be no x or y properties on the object
    with pytest.raises(AttributeError):
        assert trait.vx == 0

    with pytest.raises(AttributeError):
        assert trait.vy == 0


def test_without_position():
    """
    Validates a Position trait with required.
    """
    go = GameObject(Velocity(0, 0), Acceleration(10, 10))
    with pytest.raises(AttributeError):
        go.update_hierarchy(0)


def test_without_velocity():
    """
    Validates a Velocity trait with required.
    """
    go = GameObject(Position(10, 20), Acceleration(10, 10))
    with pytest.raises(AttributeError):
        go.update_hierarchy(0)


# noinspection PyUnresolvedReferences
def test_using_with_game_object_positive():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(
        Position(100, 100),
        Velocity(0, 0),
        Acceleration(10, 20))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 0
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 20

    # Update with 0 makes no changes
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 0
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 10
    assert go.vy == 20
    assert go.ax == 10
    assert go.ay == 20

    # Run a few more
    go.update_hierarchy(1)
    go.update_hierarchy(1)
    assert go.x == 130
    assert go.y == 160
    assert go.vx == 30
    assert go.vy == 60
    assert go.ax == 10
    assert go.ay == 20

    # Run 2 seconds
    go.update_hierarchy(2)
    assert go.x == 190
    assert go.y == 280
    assert go.vx == 50
    assert go.vy == 100
    assert go.ax == 10
    assert go.ay == 20

    # Run a half second
    go.update_hierarchy(0.5)
    assert go.x == 215
    assert go.y == 330
    assert go.vx == 55
    assert go.vy == 110
    assert go.ax == 10
    assert go.ay == 20

    # Change acceleration
    go.ax = 1
    go.ay = 2
    go.update_hierarchy(1)
    assert go.x == 270
    assert go.y == 440
    assert go.vx == 56
    assert go.vy == 112
    assert go.ax == 1
    assert go.ay == 2


# noinspection PyUnresolvedReferences
def test_using_with_game_object_negative():
    """
    Validates it can be used as a GameObject trait.
    """
    go = GameObject(
        Position(100, 100),
        Velocity(0, 0),
        Acceleration(-10, -20))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 0
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == -20

    # Update with 0 makes no changes
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    go.update_hierarchy(0)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 0
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == -20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == -10
    assert go.vy == -20
    assert go.ax == -10
    assert go.ay == -20

    # Run a few more
    go.update_hierarchy(1)
    go.update_hierarchy(1)
    assert go.x == 70
    assert go.y == 40
    assert go.vx == -30
    assert go.vy == -60
    assert go.ax == -10
    assert go.ay == -20

    # Run 2 seconds
    go.update_hierarchy(2)
    assert go.x == 10
    assert go.y == -80
    assert go.vx == -50
    assert go.vy == -100
    assert go.ax == -10
    assert go.ay == -20

    # Run a half second
    go.update_hierarchy(0.5)
    assert go.x == -15
    assert go.y == -130
    assert go.vx == -55
    assert go.vy == -110
    assert go.ax == -10
    assert go.ay == -20

    # Change acceleration
    go.ax = -1
    go.ay = -2
    go.update_hierarchy(1)
    assert go.x == -70
    assert go.y == -240
    assert go.vx == -56
    assert go.vy == -112
    assert go.ax == -1
    assert go.ay == -2


# noinspection PyUnresolvedReferences
def test_trait_order_matters():
    """
    Validates that the order traits are added matters.
    """
    go = GameObject(
        Position(100, 100),
        Velocity(0, 0),
        Acceleration(10, 20))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 0
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 10
    assert go.vy == 20
    assert go.ax == 10
    assert go.ay == 20

    # Switch Velocity and Acceleration
    go = GameObject(
        Position(100, 100),
        Acceleration(10, 20),
        Velocity(0, 0))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 0
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 20

    # Update with 1 makes changes
    go.update_hierarchy(1)
    assert go.x == 110
    assert go.y == 120
    assert go.vx == 10
    assert go.vy == 20
    assert go.ax == 10
    assert go.ay == 20


# noinspection PyUnresolvedReferences
def test_acceleration_and_friction_together():
    """
    Validates how acceleration and friction interact. These are relatively
    simple tests as it can get quite complex quite quickly.
    """
    go = GameObject(
        Position(100, 100),
        Velocity(10, 10),
        Friction(1, 2),
        Acceleration(10, 20))
    assert go.x == 100
    assert go.y == 100
    assert go.vx == 10
    assert go.vy == 10
    assert go.fx == 1
    assert go.fy == 2
    assert go.ax == 10
    assert go.ay == 20

    # Update for 1 second
    go.update_hierarchy(1)
    assert go.x == 110
    assert go.y == 110
    assert go.vx == 19
    assert go.vy == 28
    assert go.fx == 1
    assert go.fy == 2
    assert go.ax == 10
    assert go.ay == 20

    # Update for another second
    go.update_hierarchy(1)
    assert go.x == 129
    assert go.y == 138
    assert go.vx == 28
    assert go.vy == 46
    assert go.fx == 1
    assert go.fy == 2
    assert go.ax == 10
    assert go.ay == 20
