"""
Creates a large number of GameObjects to see memory usage and
performance impact
"""
import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject


def setup(game: Game):
    for _ in range(200):
        game.add_child(GameObject())


if utils.should_execute(__name__):
    utils.execute(setup)
