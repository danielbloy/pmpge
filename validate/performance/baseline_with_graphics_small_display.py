import validate.utils as utils
from pmpge.game import Game
from validate.test_data import create_test_data

SCREEN_WIDTH = 80  # Results in a border of 40 pixels left and right
SCREEN_HEIGHT = 100  # Results in a border of 14 pixels top and bottom


def setup(game: Game):
    create_test_data(game, include_graphics=True)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
