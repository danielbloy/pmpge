"""
This is a slightly different test as it creates a range of sprites and
keeps them on the screen, orbiting and following each other. This is useful
as a test of framerate where the sprites all stay in the screen.
"""
import math

import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import AngularMotion, AngularRelativeToParent, FollowSprite

sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(80, 60, 0, 0, "alien.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_b.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_c.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_d.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_e.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_f.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_g.png"),
    utils.SpriteData(80, 60, 0, 0, "alien_h.png"),
]


def setup(game: Game):
    game.background_colour = (0, 0, 0)  # Black

    # We create the sprites manually here as we don't want velocity
    for data in sprite_data:
        sprite = Sprite(
            data.x, data.y,
            DrawImage(data.image))
        data.sprite = sprite
        game.add_child(sprite)

    # Add two earth and moon sprites that orbit the centre of the screen.
    earth = Sprite(
        0, 0,
        AngularMotion(80, 60, 50, math.pi / 4),
        DrawImage("earth.png"))
    game.add_child(earth)

    moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 20, math.pi),
        DrawImage("moon.png"))
    earth.add_child(moon)

    earth2 = Sprite(
        0, 0,
        AngularMotion(80, 60, 50, math.pi / 4, start_angle=math.pi),
        DrawImage("earth.png"))
    game.add_child(earth2)

    moon2 = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 20, math.pi),
        DrawImage("moon.png"))
    earth2.add_child(moon2)

    sprite_data[0].sprite.apply_trait(FollowSprite(earth, 30, 10))
    sprite_data[1].sprite.apply_trait(FollowSprite(earth, 10, 30))

    sprite_data[2].sprite.apply_trait(FollowSprite(moon, 30, 10))
    sprite_data[3].sprite.apply_trait(FollowSprite(moon, 10, 30))

    sprite_data[4].sprite.apply_trait(FollowSprite(earth2, 30, 10))
    sprite_data[5].sprite.apply_trait(FollowSprite(earth2, 10, 30))

    sprite_data[6].sprite.apply_trait(FollowSprite(moon2, 30, 10))
    sprite_data[7].sprite.apply_trait(FollowSprite(moon2, 10, 30))


if utils.should_execute(__name__):
    utils.execute(setup)
