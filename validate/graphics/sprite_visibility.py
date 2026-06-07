"""
Creates sprites and on the screen, alternating visibility. This test also
uses the same resource for each sprite which can be used to validate
optimisations on image resource sharing. This is useful for visually checking
that visibility works.
"""

import validate.utils as utils
from pmpge.game import Game
from validate import test_data

sprite_data: list[test_data.SpriteData] = [
    test_data.SpriteData(20, 20, "alien.png"),
    test_data.SpriteData(60, 20, "alien.png"),
    test_data.SpriteData(100, 20, "alien.png"),
    test_data.SpriteData(140, 20, "alien.png"),
    test_data.SpriteData(20, 60, "alien.png"),
    test_data.SpriteData(60, 60, "alien.png"),
    test_data.SpriteData(100, 60, "alien.png"),
    test_data.SpriteData(140, 60, "alien.png"),
    test_data.SpriteData(20, 100, "alien.png"),
    test_data.SpriteData(60, 100, "alien.png"),
    test_data.SpriteData(100, 100, "alien.png"),
    test_data.SpriteData(140, 100, "alien.png"),
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
