import validate.utils as utils
from pmpge.game import Game
from validate.test_data import create_memory_limit_test_data

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120


def setup(game: Game):
    create_memory_limit_test_data(game, include_graphics=True)


if utils.should_execute(__name__):
    utils.execute(setup, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)
