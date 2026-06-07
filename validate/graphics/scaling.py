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
    test_data.SpriteData(15, 15, "alien.png"),
    test_data.SpriteData(65, 15, "alien_b.png"),
    test_data.SpriteData(15, 50, "alien_c.png"),
    test_data.SpriteData(65, 50, "alien_d.png"),
]

index = 0
count = len(sprite_data)

SCREEN_WIDTH = 80  # Required for validate_all.py
SCREEN_HEIGHT = 64  # Required for validate_all.py


def switch_visibility(game: Game):
    global index
    sprite_data[index].sprite.visible = True
    index = (index + 1) % count
    sprite_data[index].sprite.visible = False


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    utils.create_sprites(game, sprite_data)
    utils.add_update_method(game, switch_visibility, fps=4)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
