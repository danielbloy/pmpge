"""
Creates hierarchy of GameObjects to see memory usage and
performance impact.
"""
import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject


def setup(game: Game):
    for _ in range(10):
        children = [
            GameObject(
                children=[GameObject() for _ in range(2)]
            ) for _ in range(3)
        ]
        game.add_child(GameObject(children=children))


if utils.should_execute(__name__):
    utils.execute(setup)
