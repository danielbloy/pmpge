import math

import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.sprite import Sprite
from pmpge.traits.physics import AngularMotion
from pmpge.traits.position import Position, AngularRelativeToParent
from tests.pmpge.testing_utilities import are_almost_equal


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    trait = AngularMotion(0, 0, 0, 0)
    assert trait.cx == 0
    assert trait.cy == 0
    assert trait.radius == 0
    assert trait.angular_velocity == 0
    assert trait.angle == 0

    trait = AngularMotion(10, 20, 30, 40.5)
    assert trait.cx == 10
    assert trait.cy == 20
    assert trait.radius == 30
    assert trait.angular_velocity == 40.5
    assert trait.angle == 0

    trait = AngularMotion(-10, -20, -30, -40, 5.0)
    assert trait.cx == -10
    assert trait.cy == -20
    assert trait.radius == -30
    assert trait.angular_velocity == -40
    assert trait.angle == 5.0

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
    go = GameObject(Position(100, 100), AngularMotion(10, 20, 30, math.pi))
    assert go.x == 100
    assert go.y == 100
    assert go.cx == 10
    assert go.cy == 20
    assert go.radius == 30
    assert go.angular_velocity == math.pi
    assert go.angle == 0


# noinspection PyUnresolvedReferences
def test_works_with_sprite():
    """
    Validates the trait works with a Sprite.
    """
    go = Sprite(100, 100, AngularMotion(10, 20, 30, math.pi))
    assert go.x == 100
    assert go.y == 100
    assert go.cx == 10
    assert go.cy == 20
    assert go.radius == 30
    assert go.angular_velocity == math.pi
    assert go.angle == 0


def test_angular_motion():
    """
    Validates that the angular motion is correctly calculated.
    """
    trait = AngularMotion(100, 100, 30, math.pi)
    assert trait.cx == 100
    assert trait.cy == 100
    assert trait.radius == 30
    assert trait.angular_velocity == math.pi
    assert trait.angle == 0

    trait.update(1)
    assert are_almost_equal(trait.x, 70)
    assert are_almost_equal(trait.y, 100)
    assert are_almost_equal(trait.angle, math.pi)

    trait.update(1)
    assert are_almost_equal(trait.x, 130)
    assert are_almost_equal(trait.y, 100)
    assert are_almost_equal(trait.angle, 2 * math.pi)

    trait.update(1)
    assert are_almost_equal(trait.x, 70)
    assert are_almost_equal(trait.y, 100)
    assert are_almost_equal(trait.angle, 3 * math.pi)

    # Now offset so we rotate the y coordinate
    trait.update(0.5)
    assert are_almost_equal(trait.x, 100)
    assert are_almost_equal(trait.y, 70)
    assert are_almost_equal(trait.angle, 3.5 * math.pi)

    trait.update(1)
    assert are_almost_equal(trait.x, 100)
    assert are_almost_equal(trait.y, 130)
    assert are_almost_equal(trait.angle, 4.5 * math.pi)

    trait.update(1)
    assert are_almost_equal(trait.x, 100)
    assert are_almost_equal(trait.y, 70)
    assert are_almost_equal(trait.angle, 5.5 * math.pi)

    # Now shorten the radius
    trait.radius = 10
    trait.update(1)
    assert are_almost_equal(trait.x, 100)
    assert are_almost_equal(trait.y, 110)
    assert are_almost_equal(trait.angle, 6.5 * math.pi)

    # Finally, we test the start angle
    trait = AngularMotion(100, 100, 30, math.pi, math.pi / 2)
    trait.update(1)
    assert are_almost_equal(trait.x, 100)
    assert are_almost_equal(trait.y, 70)
    assert are_almost_equal(trait.angle, 1.5 * math.pi)


# noinspection PyUnresolvedReferences
def test_relative_to_parent():
    """
    Some simple checks on the AngularRelativeToParent class. All it does is update
    the (cx, cy) position based on the parent. It's designed to be used with a
    GameObject that has a position
    """
    parent = GameObject(Position(100, 100))

    child = GameObject(AngularRelativeToParent, parent=parent)
    # The dt value makes no different
    update_hierarchy(child, 0)
    assert child.cx == 100
    assert child.cy == 100

    update_hierarchy(child, 1)
    assert child.cx == 100
    assert child.cy == 100

    # Move parent and watch us follow
    parent.x = 50
    parent.y = 150
    update_hierarchy(child, 0)
    assert child.cx == 50
    assert child.cy == 150
