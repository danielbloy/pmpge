"""
Creates a moderate number of root GameObjects all as children to the
root object. There are no traits or anything here.
"""
import validate.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject


def setup(game: Game):
    for _ in range(100):
        game.add_child(GameObject())


if utils.should_execute(__name__):
    utils.execute(setup)
