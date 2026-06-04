import math

import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import AngularMotion, AngularRelativeToParent, FollowSprite
from pmpge.traits.position import HorizontalOscillator, VerticalOscillator


def create_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created:
        - Two Earth sprites orbiting the centre of the screen (earth_1, earth_2)
        - Two Moon sprites orbiting their respective Earth sprites
        - Eight Alien sprites following their respective Earth and Moon sprites (2 each)
        - 2 sprites oscillating horizontrally at the top of the screen
        - 2 sprites oscillating horizontrally at the bottom of the screen
        - 2 sprites oscillating vertically at the left of the screen
        - 2 sprites oscillating vertically at the right of the screen
    """
    game.background_colour = (250, 120, 0)  # Orange

    earth_1 = Sprite(0, 0, AngularMotion(game.width // 2, game.height // 2, 25, math.pi / 4))
    if include_graphics:
        earth_1.apply_trait(DrawImage("earth.png"))

    earth_2 = Sprite(
        0, 0,
        AngularMotion(game.width // 2, game.height // 2, 25, math.pi / 4, start_angle=math.pi))
    if include_graphics:
        earth_2.apply_trait(DrawImage("earth.png"))

    earth_1_moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 15, math.pi))
    if include_graphics:
        earth_1_moon.apply_trait(DrawImage("moon.png"))

    earth_2_moon = Sprite(
        0, 0,
        AngularRelativeToParent(),
        AngularMotion(0, 0, 15, math.pi))
    if include_graphics:
        earth_2_moon.apply_trait(DrawImage("moon.png"))

    game.add_child(earth_1)
    game.add_child(earth_2)
    earth_1.add_child(earth_1_moon)
    earth_2.add_child(earth_2_moon)

    # We create the follow sprites manually as we don't want the velocity trait.
    follow_sprites: list[utils.SpriteData] = [
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "7x3.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "john.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "8x8.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "7x7.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "7x3.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "8x8.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "hero_front.png"),
        utils.SpriteData(game.width // 2, game.height // 2, 0, 0, "7x7.png"),
    ]

    for data in follow_sprites:
        sprite = Sprite(data.x, data.y)
        data.sprite = sprite

        if include_graphics:
            sprite.apply_trait(DrawImage(data.image))

    for item in enumerate([earth_1, earth_1, earth_1_moon, earth_1_moon, earth_2, earth_2, earth_2_moon, earth_2_moon]):
        index = item[0]
        parent = item[1]
        vx = 30 if index % 2 == 0 else 10
        vy = 10 if index % 2 == 0 else 30
        follow_sprites[index].sprite.apply_trait(FollowSprite(parent, vx, vy))
        parent.add_child(follow_sprites[index].sprite)

    # Add in the horizontally and vertically oscillating sprites.
    move_sprites: list[utils.SpriteData] = [
        utils.SpriteData(5, 5, 30, 0, "x.png"),
        utils.SpriteData(game.width - 5, 5, -30, 0, "y.png"),
        utils.SpriteData(5, game.height - 5, 30, 0, "a.png"),
        utils.SpriteData(game.width - 5, game.height - 5, -30, 0, "b.png"),
        utils.SpriteData(5, 5, 0, 30, "l.png"),
        utils.SpriteData(game.width - 5, 5, 0, 30, "r.png"),
        utils.SpriteData(5, game.height - 5, 0, -30, "u.png"),
        utils.SpriteData(game.width - 5, game.height - 5, 0, -30, "d.png"),
    ]

    utils.create_sprites(game, move_sprites, include_graphics=include_graphics)
    horizontal_trait = HorizontalOscillator(10, game.width - 10)
    vertical_trait = VerticalOscillator(10, game.height - 10)

    for sprite in move_sprites:
        sprite.sprite.apply_trait(horizontal_trait)
        sprite.sprite.apply_trait(vertical_trait)
