import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.sprite import Sprite
from pmpge.traits.position import FollowSprite, Position


def test_constructor():
    """
    Simple test to ensure that constructor works.
    """
    target = Sprite(100, 100)
    trait = FollowSprite(target, 0, 0)
    assert trait.vx == 0
    assert trait.vy == 0
    assert trait.target == target

    trait = FollowSprite(target, 10, 20)
    assert trait.vx == 10
    assert trait.vy == 20
    assert trait.target == target


def test_without_position():
    """
    Validates a Position trait with required.
    """
    target = Sprite(100, 100)
    go = GameObject(FollowSprite(target, 10, 20))
    with pytest.raises(AttributeError):
        update_hierarchy(go, 0)


# noinspection PyUnresolvedReferences
def test_works_with_game_object():
    """
    Validates the trait works with a GameObject.
    """
    target = Sprite(100, 100)

    go = GameObject(Position(0, 0), FollowSprite(target, 10, 50))
    assert go.x == 0
    assert go.y == 0
    assert go.vx == 10
    assert go.vy == 50

    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 50
    assert go.vx == 10
    assert go.vy == 50


# noinspection PyUnresolvedReferences
def test_works_with_sprite():
    """
    Validates the trait works with a Sprite.
    """
    target = Sprite(100, 100)

    go = Sprite(0, 0, FollowSprite(target, 10, 50))
    assert go.x == 0
    assert go.y == 0
    assert go.vx == 10
    assert go.vy == 50

    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 50
    assert go.vx == 10
    assert go.vy == 50


# noinspection PyUnresolvedReferences
def test_follow_sprite_up():
    """
    Validates the sprite follows up at the correct speed
    """
    target = Sprite(100, 100)

    go = GameObject(Position(100, 0), FollowSprite(target, 10, 50))
    update_hierarchy(go, 1)
    assert go.x == 100
    assert go.y == 50
    assert go.vx == 10
    assert go.vy == 50


# noinspection PyUnresolvedReferences
def test_follow_sprite_down():
    """
    Validates the sprite follows down at the correct speed.
    """
    target = Sprite(100, 100)

    go = GameObject(Position(100, 200), FollowSprite(target, 10, 100))
    update_hierarchy(go, 0.25)
    assert go.x == 100
    assert go.y == 175
    assert go.vx == 10
    assert go.vy == 100


# noinspection PyUnresolvedReferences
def test_follow_sprite_left():
    """
    Validates the sprite follows left at the correct speed.
    """
    target = Sprite(100, 100)

    go = GameObject(Position(200, 100), FollowSprite(target, 20, 50))
    update_hierarchy(go, 2)
    assert go.x == 160
    assert go.y == 100
    assert go.vx == 20
    assert go.vy == 50


# noinspection PyUnresolvedReferences
def test_follow_sprite_right():
    """
    Validates the sprite follows right at the correct speed.
    """
    target = Sprite(100, 100)

    go = GameObject(Position(0, 100), FollowSprite(target, 30, 50))
    update_hierarchy(go, 0.5)
    assert go.x == 15
    assert go.y == 100
    assert go.vx == 30
    assert go.vy == 50


# noinspection PyUnresolvedReferences
def test_follows_correct_sprite():
    """
    Validates the sprite follows correctly.
    """
    target = Sprite(100, 100)
    other = Sprite(700, 700)

    go = GameObject(Position(500, 500), FollowSprite(target, 100, 100))
    update_hierarchy(go, 1)
    assert go.x == 400
    assert go.y == 400
    assert go.vx == 100
    assert go.vy == 100


# noinspection PyUnresolvedReferences
def test_follows_changes_direction():
    """
    Validates that when the sprite being followed moves, the direction changes.
    """
    target = Position(0, 0)

    # Move up and left
    go = GameObject(Position(100, 100), FollowSprite(target, 10, 20))
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 80
    update_hierarchy(go, 1)
    assert go.x == 80
    assert go.y == 60

    # Move target to the right
    target.x = 200
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 40

    # Move target down
    target.y = 200
    update_hierarchy(go, 1)
    assert go.x == 100
    assert go.y == 60
    update_hierarchy(go, 1)
    assert go.x == 110
    assert go.y == 80

    # Move target to the left
    target.x = 0
    update_hierarchy(go, 1)
    assert go.x == 100
    assert go.y == 100
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 120

    # Move target back to the starting position
    target.y = 0
    update_hierarchy(go, 1)
    assert go.x == 80
    assert go.y == 100


# noinspection PyUnresolvedReferences
def test_changes_speed():
    """
    Validates that when the chase speed is changed, this is reflected in the trait.
    """
    target = Position(0, 0)

    go = GameObject(Position(100, 100), FollowSprite(target, 10, 20))
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 80
    update_hierarchy(go, 1)
    assert go.x == 80
    assert go.y == 60

    # Now change y speed
    go.vy = 10
    update_hierarchy(go, 1)
    assert go.x == 70
    assert go.y == 50

    # Now change x speed
    go.vx = 15
    update_hierarchy(go, 1)
    assert go.x == 55
    assert go.y == 40


# noinspection PyUnresolvedReferences
def test_velocity_sign_ignored():
    """
    Validates that negative velocity values are treated the same as positive ones.
    """
    target = Position(0, 0)

    go = GameObject(Position(100, 100), FollowSprite(target, -10, -10))
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 90

    update_hierarchy(go, 1)
    assert go.x == 80
    assert go.y == 80

    go.vx = -10
    update_hierarchy(go, 1)
    assert go.x == 70
    assert go.y == 70

    go.vy = -5
    update_hierarchy(go, 1)
    assert go.x == 60
    assert go.y == 65


# noinspection PyUnresolvedReferences
def test_stops_when_reaches_target():
    """
    Validates that when the target is reached, the sprite stops.
    """
    target = Position(0, 0)

    go = GameObject(Position(20, 20), FollowSprite(target, 10, 10))
    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 10

    update_hierarchy(go, 1)
    assert go.x == 0
    assert go.y == 0

    # This should do nothing
    update_hierarchy(go, 1)
    assert go.x == 0
    assert go.y == 0


# noinspection PyUnresolvedReferences
def test_no_flip_flop():
    """
    Validates that when the sprite is caught but the velocity would take it past the
    target, it stops. We do this from all 4 directions.
    """
    target = Position(10, 10)

    go = GameObject(Position(5, 5), FollowSprite(target, 10, 10))
    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 10

    go = GameObject(Position(15, 15), FollowSprite(target, 10, 10))
    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 10

    go = GameObject(Position(15, 5), FollowSprite(target, 10, 10))
    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 10

    go = GameObject(Position(5, 15), FollowSprite(target, 10, 10))
    update_hierarchy(go, 1)
    assert go.x == 10
    assert go.y == 10


# noinspection PyUnresolvedReferences
def test_follows_new_sprite():
    """
    Validates that when the sprite being follows changes, it is correctly
    picked up.
    """
    target1 = Position(0, 0)
    target2 = Position(200, 200)

    go = GameObject(Position(100, 100), FollowSprite(target1, 10, 10))
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 90
    update_hierarchy(go, 1)
    assert go.x == 80
    assert go.y == 80

    # Now change target
    go.target = target2
    update_hierarchy(go, 1)
    assert go.x == 90
    assert go.y == 90

    update_hierarchy(go, 1)
    assert go.x == 100
    assert go.y == 100
