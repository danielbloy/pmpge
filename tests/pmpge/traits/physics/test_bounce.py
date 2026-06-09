import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.sprite import Sprite
from pmpge.traits.physics import HorizontalBounce, VerticalBounce, Velocity


def test_horizontal_bounce_constructor():
    """
    Simple test to ensure the constructor works.
    """
    trait = HorizontalBounce(1, 2)
    assert trait.limits_x == (1, 2)

    # Can't have a max_x that is less than a min_x
    with pytest.raises(ValueError):
        HorizontalBounce(2, 1)


def test_vertical_bounce_constructor():
    """
    Simple test to ensure the constructor works.
    """
    trait = VerticalBounce(1, 2)
    assert trait.limits_y == (1, 2)

    # Can't have a max_x that is less than a min_x
    with pytest.raises(ValueError):
        VerticalBounce(2, 1)


def test_horizontal_bounce_without_velocity():
    """
    Validates a Velocity trait is required.
    """
    go = GameObject(HorizontalBounce(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


def test_vertical_bounce_without_velocity():
    """
    Validates a Velocity trait is required.
    """
    go = GameObject(VerticalBounce(10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


# noinspection PyUnresolvedReferences
def test_horizontal_bounce():
    """
    Some simple tests to ensure it bounces at the limit.
    """
    go = Sprite(0, 0, Velocity(10, 20), HorizontalBounce(10, 20))
    update_hierarchy(go, 2)
    assert go.x == 20
    assert go.y == 40
    assert go.vx == 10
    assert go.vy == 20

    # The next update should result in a bounce
    update_hierarchy(go, 0.1)
    assert go.x == 21
    assert go.y == 42
    assert go.vx == -10
    assert go.vy == 20

    # Now we go back
    update_hierarchy(go, 1)
    assert go.x == 11
    assert go.y == 62
    assert go.vx == -10
    assert go.vy == 20

    # Now over the threshold
    update_hierarchy(go, 0.2)
    assert go.x == 9
    assert go.y == 66
    assert go.vx == 10
    assert go.vy == 20


# noinspection PyUnresolvedReferences
def test_vertical_bounce():
    """
    Some simple tests to ensure it bounces at the limit.
    """
    go = Sprite(0, 0, Velocity(10, 20), VerticalBounce(10, 40))
    update_hierarchy(go, 2)
    assert go.x == 20
    assert go.y == 40
    assert go.vx == 10
    assert go.vy == 20

    # The next update should result in a bounce
    update_hierarchy(go, 0.1)
    assert go.x == 21
    assert go.y == 42
    assert go.vx == 10
    assert go.vy == -20

    # Now we go back
    update_hierarchy(go, 1.5)
    assert go.x == 36
    assert go.y == 12
    assert go.vx == 10
    assert go.vy == -20

    # Now over the threshold
    update_hierarchy(go, 0.2)
    assert go.x == 38
    assert go.y == 8
    assert go.vx == 10
    assert go.vy == 20
