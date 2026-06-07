"""
Creates sprite in the center of the screen and allows the controller
to move it around. The other buttons toggle the visibility of sprites.
"""
import validate.utils as utils
from pmpge.game import Game
from validate.test_data import create_controller_test_data


def setup(game: Game):
    game.background_colour = (250, 120, 0)  # Orange
    create_controller_test_data(game, include_graphics=True)


if utils.should_execute(__name__):
    utils.execute(setup)
