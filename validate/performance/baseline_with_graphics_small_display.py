from validate_device.test_data.test_data import create_test_data

import validate_device.utils as utils
from pmpge.game import Game

SCREEN_WIDTH = 80  # Results in a border of 40 pixels left and right
SCREEN_HEIGHT = 100  # Results in a border of 14 pixels top and bottom


def setup(game: Game):
    create_test_data(game, include_graphics=True)


if utils.should_execute(__name__):
    utils.execute(setup)
