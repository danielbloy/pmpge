import tests.validate_device.utils as utils
from pmpge.game import Game
from tests.validate_device.performance.test_data import create_test_data


def setup(game: Game):
    create_test_data(game, include_graphics=False)


if utils.should_execute(__name__):
    utils.execute(setup)
