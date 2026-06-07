from tests.validate_device.test_data.test_data import create_test_data

import validate_device.utils as utils
from pmpge.game import Game


def setup(game: Game):
    create_test_data(game, include_graphics=False)


if utils.should_execute(__name__):
    utils.execute(setup)
