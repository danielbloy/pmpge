"""
Creates sprites and on the screen, alternating visibility. This test also
uses the same resource for each sprite which can be used to validate
optimisations on image resource sharing.
"""

import tests.validate_device.utils as utils
from pmpge.game import Game

sprite_data: list[utils.SpriteData] = [
    utils.SpriteData(20, 20, 0, 0, "alien.png"),
    utils.SpriteData(60, 20, 0, 0, "alien.png"),
    utils.SpriteData(100, 20, 0, 0, "alien.png"),
    utils.SpriteData(140, 20, 0, 0, "alien.png"),
    utils.SpriteData(20, 60, 0, 0, "alien.png"),
    utils.SpriteData(60, 60, 0, 0, "alien.png"),
    utils.SpriteData(100, 60, 0, 0, "alien.png"),
    utils.SpriteData(140, 60, 0, 0, "alien.png"),
    utils.SpriteData(20, 100, 0, 0, "alien.png"),
    utils.SpriteData(60, 100, 0, 0, "alien.png"),
    utils.SpriteData(100, 100, 0, 0, "alien.png"),
    utils.SpriteData(140, 100, 0, 0, "alien.png"),
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
    utils.add_update_method(game, switch_visibility, fps=12)


if utils.should_execute(__name__):
    utils.execute(setup)
