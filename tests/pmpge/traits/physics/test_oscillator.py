import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.sprite import Sprite
from pmpge.traits.physics import Acceleration
from pmpge.traits.physics import HorizontalOscillator, VerticalOscillator, Velocity


def test_horizontal_oscillator_constructor():
    """
    Simple test to ensure the constructor works.
    """
    trait = HorizontalOscillator(1, 2)
    assert trait.limits_x == (1, 2)

    # Can't have a max_x that is less than a min_x
    with pytest.raises(ValueError):
        HorizontalOscillator(2, 1)


def test_vertical_oscillator_constructor():
    """
    Simple test to ensure the constructor works.
    """
    trait = VerticalOscillator(1, 2)
    assert trait.limits_y == (1, 2)

    # Can't have a max_x that is less than a min_x
    with pytest.raises(ValueError):
        VerticalOscillator(2, 1)


def test_horizontal_oscillator_without_velocity():
    """
    Validates a Accelerate trait is required.
    """
    go = GameObject(HorizontalOscillator(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


def test_vertical_oscillator_without_velocity():
    """
    Validates a Accelerate trait is required.
    """
    go = GameObject(VerticalOscillator(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


# noinspection PyUnresolvedReferences
def test_horizontal_oscillator_hit_max():
    """
    Some simple tests to ensure it oscillates at the limit.
    """
    go = Sprite(0, 0, Velocity(0, 0), Acceleration(10, 0), HorizontalOscillator(10, 20))
    update_hierarchy(go, 1)
    assert go.x == 0
    assert go.y == 0
    assert go.vx == 10
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 0

    update_hierarchy(go, 2)
    assert go.x == 20
    assert go.y == 0
    assert go.vx == 30
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 0

    # The next update should result in a bounce
    update_hierarchy(go, 0.1)
    assert go.x == 23
    assert go.y == 0
    assert go.vx == 31
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == 0

    # Now go backwards
    update_hierarchy(go, 2)
    assert go.x == 85
    assert go.y == 0
    assert go.vx == 11
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == 0

    update_hierarchy(go, 0.2)
    assert go.x == 87.2
    assert go.y == 0
    assert go.vx == 9
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == 0


# noinspection PyUnresolvedReferences
def test_horizontal_oscillator_hit_min():
    """
    Some simple tests to ensure it oscillates at the limit.
    """
    go = Sprite(30, 0, Velocity(0, 0), Acceleration(-10, 0), HorizontalOscillator(10, 20))
    update_hierarchy(go, 1)
    assert go.x == 30
    assert go.y == 0
    assert go.vx == -10
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == 0

    update_hierarchy(go, 2)
    assert go.x == 10
    assert go.y == 0
    assert go.vx == -30
    assert go.vy == 0
    assert go.ax == -10
    assert go.ay == 0

    # The next update should result in a bounce
    update_hierarchy(go, 0.1)
    assert go.x == 7
    assert go.y == 0
    assert go.vx == -31
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 0

    # Now go backwards
    update_hierarchy(go, 0.1)
    assert go.x == 3.9
    assert go.y == 0
    assert go.vx == -30
    assert go.vy == 0
    assert go.ax == 10
    assert go.ay == 0


# noinspection PyUnresolvedReferences
def test_vertical_oscillator_hit_max():
    """
    Some simple tests to ensure it oscillates at the limit.
    """
    go = Sprite(0, 0, Velocity(0, 0), Acceleration(0, 10), VerticalOscillator(10, 20))
    update_hierarchy(go, 1)
    assert go.x == 0
    assert go.y == 0
    assert go.vx == 0
    assert go.vy == 10
    assert go.ax == 0
    assert go.ay == 10

    update_hierarchy(go, 2)
    assert go.x == 0
    assert go.y == 20
    assert go.vx == 0
    assert go.vy == 30
    assert go.ax == 0
    assert go.ay == 10

    # The next update should result in a bounce
    update_hierarchy(go, 0.1)
    assert go.x == 0
    assert go.y == 23
    assert go.vx == 0
    assert go.vy == 31
    assert go.ax == 0
    assert go.ay == -10

    # Now go backwards
    update_hierarchy(go, 2)
    assert go.x == 0
    assert go.y == 85
    assert go.vx == 0
    assert go.vy == 11
    assert go.ax == 0
    assert go.ay == -10

    update_hierarchy(go, 0.2)
    assert go.x == 0
    assert go.y == 87.2
    assert go.vx == 0
    assert go.vy == 9
    assert go.ax == 0
    assert go.ay == -10


# noinspection PyUnresolvedReferences
def test_vertical_oscillator_hit_min():
    """
    Some simple tests to ensure it oscillates at the limit.
    """
    go = Sprite(0, 30, Velocity(0, 0), Acceleration(0, -10), VerticalOscillator(10, 20))
    update_hierarchy(go, 1)
    assert go.x == 0
    assert go.y == 30
    assert go.vx == 0
    assert go.vy == -10
    assert go.ax == 0
    assert go.ay == -10

    update_hierarchy(go, 2)
    assert go.x == 0
    assert go.y == 10
    assert go.vx == 0
    assert go.vy == -30
    assert go.ax == 0
    assert go.ay == -10

    # The next update should result in a bounce
    update_hierarchy(go, 0.1)
    assert go.x == 0
    assert go.y == 7
    assert go.vx == 0
    assert go.vy == -31
    assert go.ax == 0
    assert go.ay == 10

    # Now go backwards
    update_hierarchy(go, 0.1)
    assert go.x == 0
    assert go.y == 3.9
    assert go.vx == 0
    assert go.vy == -30
    assert go.ax == 0
    assert go.ay == 10
