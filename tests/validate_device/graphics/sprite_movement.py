"""
Creates sprites and moves them around on the screen, alternating visibility.
"""

import tests.validate_device.utils as utils
from pmpge.game import Game

sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(80, 60, 15, 0, "alien.png"),
    utils.SpriteData(80, 60, -15, 0, "alien_b.png"),
    utils.SpriteData(80, 60, 0, 15, "alien_c.png"),
    utils.SpriteData(80, 60, 0, -15, "alien_d.png"),
    utils.SpriteData(80, 60, 15, 15, "alien_e.png"),
    utils.SpriteData(80, 60, -15, -15, "alien_f.png"),
    utils.SpriteData(80, 60, 15, -15, "alien_g.png"),
    utils.SpriteData(80, 60, -15, 15, "alien_h.png"),
]

index = 0
count = len(sprite_data)


def switch_visibility(game: Game):
    global index
    sprite_data[index].sprite.visible = True
    index = (index + 1) % count
    sprite_data[index].sprite.visible = False


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.create_sprites(game, sprite_data)
    utils.add_update_method(game, switch_visibility)


if utils.should_execute(__name__):
    utils.execute(setup)
