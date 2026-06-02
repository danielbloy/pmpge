"""
Creates hierarchy of 20 GameObjects with a typical set of traits. All of
the objects stay in the screen to push the drawing limits of the screen hard.

The sprites are in sets that orbit, follow, or simply move around the screen.
"""
import math

import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import AngularMotion, AngularRelativeToParent, FollowSprite


def create_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created:
        - Two Earth sprites orbiting the centre of the screen (earth_1, earth_2).
        - Two Moon sprites orbiting their respective Earth sprites
        - Eight Alien sprites following their respective Earth and Moon sprites
    """
    game.background_colour = (250, 120, 0)  # Orange

    earth_1 = Sprite(0, 0, AngularMotion(80, 60, 50, math.pi / 4))
    if include_graphics:
        earth_1.apply_trait(DrawImage("earth.png"))

    earth_2 = Sprite(
        0, 0,
        AngularMotion(80, 60, 50, math.pi / 4, start_angle=math.pi))
    if include_graphics:
        earth_2.apply_trait(DrawImage("earth.png"))

    earth_1_moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 20, math.pi))
    if include_graphics:
        earth_1_moon.apply_trait(DrawImage("moon.png"))

    earth_2_moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 20, math.pi))
    if include_graphics:
        earth_2_moon.apply_trait(DrawImage("moon.png"))

    game.add_child(earth_1)
    game.add_child(earth_2)
    earth_1.add_child(earth_1_moon)
    earth_2.add_child(earth_2_moon)

    follow_sprites: list[utils.SpriteData] = [
        utils.SpriteData(80, 60, 0, 0, "alien.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_b.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_c.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_d.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_e.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_f.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_g.png"),
        utils.SpriteData(80, 60, 0, 0, "alien_h.png"),
    ]

    # We create the sprites manually here as we don't want velocity
    for data in follow_sprites:
        sprite = Sprite(data.x, data.y)

        if include_graphics:
            sprite.apply_trait(DrawImage(data.image))

        data.sprite = sprite
        game.add_child(sprite)

    follow_sprites[0].sprite.apply_trait(FollowSprite(earth_1, 30, 10))
    follow_sprites[1].sprite.apply_trait(FollowSprite(earth_1, 10, 30))

    follow_sprites[2].sprite.apply_trait(FollowSprite(earth_1_moon, 30, 10))
    follow_sprites[3].sprite.apply_trait(FollowSprite(earth_1_moon, 10, 30))

    follow_sprites[4].sprite.apply_trait(FollowSprite(earth_2, 30, 10))
    follow_sprites[5].sprite.apply_trait(FollowSprite(earth_2, 10, 30))

    follow_sprites[6].sprite.apply_trait(FollowSprite(earth_2_moon, 30, 10))
    follow_sprites[7].sprite.apply_trait(FollowSprite(earth_2_moon, 10, 30))


def setup(game: Game):
    create_test_data(game, include_graphics=False)


if utils.should_execute(__name__):
    utils.execute(setup)
