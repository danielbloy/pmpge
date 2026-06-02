import tests.validate_device.performance.baseline as baseline
import tests.validate_device.utils as utils
from pmpge.game import Game


def setup(game: Game):
    baseline.create_test_data(game, include_graphics=True)


if utils.should_execute(__name__):
    utils.execute(setup)
