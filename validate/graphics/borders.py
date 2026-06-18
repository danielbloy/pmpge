"""
Creates a non-scalable game area that is small enough to require borders
at both the top and bottom of the screen. We also place a sprite in each
corner which should be partially obscured by the borders.
"""
import validate.utils as utils
from pmpge.game import Game
from validate import test_data

SCREEN_WIDTH = 100  # Results in a border of 30 pixels left and right
SCREEN_HEIGHT = 116  # Results in a border of 8 pixels along the bottom and 4 along the top

sprite_data: list[test_data.SpriteData] = [
    test_data.SpriteData(0, 0, "alien.png"),
    test_data.SpriteData(SCREEN_WIDTH, 0, "alien_b.png"),
    test_data.SpriteData(0, SCREEN_HEIGHT, "alien_c.png"),
    test_data.SpriteData(SCREEN_WIDTH, SCREEN_HEIGHT, "alien_d.png"),
]


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    test_data.create_sprites(game, sprite_data)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
