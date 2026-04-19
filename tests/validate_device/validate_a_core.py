"""
This is the most basic test that bootstraps the application and
runs it (via utils.execute()). We do nothing else.
"""
import tests.validate_device.utils as utils
from pmpge.game import Game


def setup(game: Game):
    pass


if utils.should_execute(__name__):
    utils.execute(setup)
