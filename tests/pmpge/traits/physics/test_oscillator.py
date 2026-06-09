import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.traits.physics import HorizontalOscillator, VerticalOscillator


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
    Validates a Velocity trait is required.
    """
    go = GameObject(HorizontalOscillator(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


def test_vertical_oscillator_without_velocity():
    """
    Validates a Velocity trait is required.
    """
    go = GameObject(VerticalOscillator(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)

# TODO: Test HorizontalOscillator
# TODO: Test VerticalOscillator
