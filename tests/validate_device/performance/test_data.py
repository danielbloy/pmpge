import math

import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import AngularMotion, AngularRelativeToParent, FollowSprite
from pmpge.traits.position import HorizontalBounce, VerticalBounce
from pmpge.traits.position import HorizontalOscillator, VerticalOscillator
from traits.physics import MaxVelocity, MinVelocity


def create_test_data(game: Game, include_graphics: bool):
    """
    The following set of game_objects are created:
        - Two Earth sprites orbiting the centre of the screen (earth_1, earth_2)
        - Two Moon sprites orbiting their respective Earth sprites
        - Eight Alien sprites following their respective Earth and Moon sprites (2 each)
        - 2 sprites oscillating/bouncing horizontally at the top of the screen
        - 2 sprites oscillating/bouncing horizontally at the bottom of the screen
        - 2 sprites oscillating/bouncing vertically at the left of the screen
        - 2 sprites oscillating/bouncing vertically at the right of the screen
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

    follow_sprites: list[utils.SpriteData] = [
        utils.SpriteData(game.width // 2, game.height // 2, "7x3.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "john.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "8x8.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "7x7.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "7x3.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "8x8.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "hero_front.png"),
        utils.SpriteData(game.width // 2, game.height // 2, "7x7.png"),
    ]

    utils.create_sprites(game, follow_sprites, include_graphics=include_graphics, add_to_root=False)

    for item in enumerate([earth_1, earth_1, earth_1_moon, earth_1_moon, earth_2, earth_2, earth_2_moon, earth_2_moon]):
        index = item[0]
        parent = item[1]
        vx = 30 if index % 2 == 0 else 10
        vy = 10 if index % 2 == 0 else 30
        follow_sprites[index].sprite.apply_trait(FollowSprite(parent, vx, vy))
        parent.add_child(follow_sprites[index].sprite)

    # Add in the horizontally and vertically oscillating sprites.
    move_sprites: list[utils.SpriteData] = [
        utils.SpriteData(5, 5, "x.png", vx=30, vy=0, ax=30, ay=0),
        utils.SpriteData(game.width - 5, 5, "y.png", vx=30, vy=0),
        utils.SpriteData(game.width - 5, game.height - 5, "a.png", vx=-30, vy=0, ax=30, ay=0),
        utils.SpriteData(5, game.height - 5, "b.png", vx=-30, vy=0),
        utils.SpriteData(5, 5, "l.png", vx=0, vy=30, ax=0, ay=30),
        utils.SpriteData(game.width - 5, 5, "r.png", vx=0, vy=30),
        utils.SpriteData(game.width - 5, game.height - 5, "u.png", vx=0, vy=-30, ax=0, ay=30),
        utils.SpriteData(5, game.height - 5, "d.png", vx=0, vy=-30),
    ]

    utils.create_sprites(game, move_sprites, include_graphics=include_graphics)
    horizontal_oscillator = HorizontalOscillator(20, game.width - 20)
    vertical_oscillator = VerticalOscillator(20, game.height - 20)
    horizontal_bounce = HorizontalBounce(5, game.width - 5)
    vertical_bounce = VerticalBounce(5, game.height - 5)
    max_velocity = MaxVelocity(30, 30)
    min_velocity = MinVelocity(-30, -30)

    for item in enumerate(move_sprites):
        index = item[0]
        sprite = item[1]
        if index % 2 == 0:
            sprite.sprite.apply_trait(horizontal_oscillator)
            sprite.sprite.apply_trait(vertical_oscillator)
        else:
            sprite.sprite.apply_trait(horizontal_bounce)
            sprite.sprite.apply_trait(vertical_bounce)

        sprite.sprite.apply_trait(max_velocity)
        sprite.sprite.apply_trait(min_velocity)
