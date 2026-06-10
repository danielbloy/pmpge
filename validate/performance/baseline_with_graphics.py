import validate.utils as utils
from pmpge.game import Game
from validate.test_data import create_test_data


def setup(game: Game):
    create_test_data(game, include_graphics=True)


if utils.should_execute(__name__):
    utils.execute(setup)
