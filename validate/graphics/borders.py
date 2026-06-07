"""
Creates a non-scalable game area that is small enough to require borders
at both the top and bottom of the screen.
"""

import validate.utils as utils
from pmpge.game import Game
from validate import test_data

sprite_data: list[test_data.SpriteData] = [
    test_data.SpriteData(25, 30, "alien.png"),
    test_data.SpriteData(75, 30, "alien_b.png"),
    test_data.SpriteData(25, 80, "alien_c.png"),
    test_data.SpriteData(75, 80, "alien_d.png"),
]

index = 0
count = len(sprite_data)

SCREEN_WIDTH = 100  # Results in a border of 30 pixels left and right
SCREEN_HEIGHT = 116  # Results in a border of 8 pixels along the bottom and 4 along the top


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
