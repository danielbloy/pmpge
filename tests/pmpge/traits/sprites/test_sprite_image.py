import pytest

import pmpge.environment as environment
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.sprite import Sprite
from pmpge.traits.position import Position
from pmpge.traits.sprites import SpriteImage
from tests.pmpge.test_utilities import setup_pgzero


def test_constructor():
    """
    Simple test to ensure that DrawImage works. This pays particular attention to the
    bounding box as we need to adhere to the placement rules.
    """
    setup_pgzero(__file__)
    trait = SpriteImage("7x3.png")
    assert trait.image.surface is not None
    assert trait.image.width == 7
    assert trait.image.height == 3
    assert trait.width == 7
    assert trait.height == 3

    trait = SpriteImage("7x7.png")
    assert trait.image.surface is not None
    assert trait.image.width == 7
    assert trait.image.height == 7
    assert trait.width == 7
    assert trait.height == 7

    trait = SpriteImage("8x8.png")
    assert trait.image.surface is not None
    assert trait.image.width == 8
    assert trait.image.height == 8
    assert trait.width == 8
    assert trait.height == 8


# noinspection PyUnresolvedReferences
def test_using_with_sprite():
    """
    Validates it can be used as a Sprite trait.
    """
    setup_pgzero(__file__)
    sprite = Sprite(0, 0, SpriteImage("8x8.png"))
    assert sprite.image.surface is not None
    assert sprite.image.width == 8
    assert sprite.image.height == 8
    assert sprite.width == 8
    assert sprite.height == 8
    assert sprite.top_left == (-4, -4)
    assert sprite.bottom_right == (3, 3)

    sprite = Sprite(10, 20, SpriteImage("8x8.png"))
    assert sprite.x == 10
    assert sprite.y == 20
    assert sprite.image.surface is not None
    assert sprite.image.width == 8
    assert sprite.image.height == 8
    assert sprite.width == 8
    assert sprite.height == 8
    assert sprite.top_left == (6, 16)
    assert sprite.bottom_right == (13, 23)


# noinspection PyUnresolvedReferences
def test_changing_sprite_image():
    """
    Validates that the image can be changed.
    """
    setup_pgzero(__file__)
    sprite = Sprite(0, 0, SpriteImage("8x8.png"))
    assert sprite.image.surface is not None
    assert sprite.image.width == 8
    assert sprite.image.height == 8
    assert sprite.width == 8
    assert sprite.height == 8
    assert sprite.top_left == (-4, -4)
    assert sprite.bottom_right == (3, 3)

    sprite.image.name = "7x3.png"
    assert sprite.image.surface is not None
    assert sprite.image.width == 7
    assert sprite.image.height == 3
    assert sprite.width == 7
    assert sprite.height == 3
    assert sprite.top_left == (-3, -1)
    assert sprite.bottom_right == (3, 1)


@pytest.mark.skip(reason="this will not work with draw() disabled")
def test_draws_when_combined_with_sprite():
    """
    Validates that SpriteImage draws without throwing an exception when combined with Sprite.
    """
    setup_pgzero(__file__)
    update_counter = 2

    def draw(surface):
        nonlocal update_counter
        update_counter -= 1
        if update_counter <= 0:
            environment.terminate()

    game = Game(320, 200)
    game.add_draw_func(draw)

    setup_pgzero(__file__)
    sprite = Sprite(0, 0, SpriteImage("8x8.png"))
    game.add_child(sprite)
    game.run()


# noinspection PyUnresolvedReferences
def test_using_with_game_object():
    """
    Confirms that this cannot be used with a GameObject, even with a Position.
    """
    setup_pgzero(__file__)
    go = GameObject(Position(0, 0), SpriteImage("8x8.png"))
    assert go.image.surface is not None
    assert go.width == 8
    assert go.height == 8
    with pytest.raises(AttributeError):
        assert go.top_left == (0, 0)  # this will fail because there are no bounds properties

    with pytest.raises(AttributeError):
        go.draw_hierarchy(None)

    go.update_hierarchy(0)

    go.image.load("7x3.png")
    assert go.image.surface is not None
    assert go.image.width == 7
    assert go.image.height == 3
    with pytest.raises(AttributeError):
        assert go.top_left == (0, 0)  # this will fail because there are no bounds properties

    with pytest.raises(AttributeError):
        go.draw_hierarchy(None)


@pytest.mark.skip(reason="this will not work with draw() disabled")
def test_draws_fails_when_combined_with_game_object():
    """
    Validates that SpriteImage fails with an exception when combined with a GameObject.
    """
    setup_pgzero(__file__)
    update_counter = 2

    def draw(surface):
        nonlocal update_counter
        update_counter -= 1
        if update_counter <= 0:
            environment.terminate()

    game = Game(320, 200)
    game.add_draw_func(draw)

    setup_pgzero(__file__)
    go = GameObject(Position(0, 0), SpriteImage("8x8.png"))
    game.add_child(go)

    with pytest.raises(AttributeError):
        game.run()
