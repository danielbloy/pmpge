import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.sprite import Sprite
from pmpge.traits.physics import Velocity, BoundVelocity
from pmpge.traits.position import Position


def test_velocity_constructor():
    """
    Simple test to ensure the constructor works.
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


def test_velocity_without_position():
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


def test_bound_velocity_constructor():
    """
    Simple test to ensure the constructor works.
    """
    trait = BoundVelocity()
    assert trait.min_vx is None
    assert trait.max_vx is None
    assert trait.min_vy is None
    assert trait.max_vy is None

    trait = BoundVelocity(10)
    assert trait.min_vx == 10
    assert trait.max_vx is None
    assert trait.min_vy is None
    assert trait.max_vy is None

    trait = BoundVelocity(11, 21)
    assert trait.min_vx == 11
    assert trait.max_vx == 21
    assert trait.min_vy is None
    assert trait.max_vy is None

    # Can't have a min_vx that is lexx than a max_vx
    with pytest.raises(ValueError):
        BoundVelocity(min_vx=32, max_vx=22)

    trait = BoundVelocity(min_vy=10)
    assert trait.min_vx is None
    assert trait.max_vx is None
    assert trait.min_vy == 10
    assert trait.max_vy is None

    trait = BoundVelocity(min_vy=11, max_vy=21)
    assert trait.min_vx is None
    assert trait.max_vx is None
    assert trait.min_vy == 11
    assert trait.max_vy == 21

    # Can't have a min_vy that is lexx than a max_vy
    with pytest.raises(ValueError):
        BoundVelocity(min_vy=32, max_vy=22)

    trait = BoundVelocity(10, 20, 30, 40)
    assert trait.min_vx == 10
    assert trait.max_vx == 20
    assert trait.min_vy == 30
    assert trait.max_vy == 40

    trait = BoundVelocity(min_vx=41, max_vy=21)
    assert trait.min_vx == 41
    assert trait.max_vx is None
    assert trait.min_vy is None
    assert trait.max_vy == 21


def test_bound_velocity_without_position():
    """
    Validates a Velocity trait with required.
    """
    go = GameObject(BoundVelocity(10, 20, 10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


def test_bound_vx():
    """
    Some simple tests to ensure that vx is bound to the limits.
    """

    # Just bound min
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(min_vx=10))
    update_hierarchy(go, 0)
    assert go.vx == 10

    go.vx = 5
    update_hierarchy(go, 0)
    assert go.vx == 10

    go.vx = 15
    update_hierarchy(go, 0)
    assert go.vx == 15

    # Just max
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(max_vx=20))
    update_hierarchy(go, 0)
    assert go.vx == 0

    go.vx = 5
    update_hierarchy(go, 0)
    assert go.vx == 5

    go.vx = 25
    update_hierarchy(go, 0)
    assert go.vx == 20

    # Both min and max
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(min_vx=10, max_vx=20))
    update_hierarchy(go, 0)
    assert go.vx == 10

    go.vx = 5
    update_hierarchy(go, 0)
    assert go.vx == 10

    go.vx = 15
    update_hierarchy(go, 0)
    assert go.vx == 15

    go.vx = 25
    update_hierarchy(go, 0)
    assert go.vx == 20


def test_bound_vy():
    """
    Some simple tests to ensure that vx is bound to the limits.
    """

    # Just bound min
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(min_vy=10))
    update_hierarchy(go, 0)
    assert go.vy == 10

    go.vy = 5
    update_hierarchy(go, 0)
    assert go.vy == 10

    go.vy = 15
    update_hierarchy(go, 0)
    assert go.vy == 15

    # Just max
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(max_vy=20))
    update_hierarchy(go, 0)
    assert go.vy == 0

    go.vy = 5
    update_hierarchy(go, 0)
    assert go.vy == 5

    go.vy = 25
    update_hierarchy(go, 0)
    assert go.vy == 20

    # Both min and max
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(min_vy=10, max_vy=20))
    update_hierarchy(go, 0)
    assert go.vy == 10

    go.vy = 5
    update_hierarchy(go, 0)
    assert go.vy == 10

    go.vy = 15
    update_hierarchy(go, 0)
    assert go.vy == 15

    go.vy = 25
    update_hierarchy(go, 0)
    assert go.vy == 20


def test_bound_vx_and_vy():
    """
    Some simple tests to ensure that vx and vy are bound to the limits.
    """
    go = Sprite(100, 100, Velocity(0, 0), BoundVelocity(-30, 30, -20, 20))
    update_hierarchy(go, 0)
    assert go.vx == 0
    assert go.vy == 0

    go.vx = -30
    go.vy = 50
    update_hierarchy(go, 0)
    assert go.vx == -30
    assert go.vy == 20

    go.vx = 60
    go.vy = -57.3
    update_hierarchy(go, 0)
    assert go.vx == 30
    assert go.vy == -20

    go.vx = -10
    go.vy = -10
    update_hierarchy(go, 0)
    assert go.vx == -10
    assert go.vy == -10
