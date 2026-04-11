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

# TODO: Validate friction with zero velocity
