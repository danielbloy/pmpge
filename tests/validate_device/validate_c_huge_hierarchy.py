"""
Creates a huge hierarchy of GameObjects to see memory usage and
performance impact. This only runs on a Desktop PC usually
"""
import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject


def setup(game: Game):
    for _ in range(10):
        children = [
            GameObject(
                children=[
                    GameObject(children=[
                        GameObject(
                            children=[
                                GameObject(
                                ) for _ in range(4)
                            ]) for _ in range(5)
                    ]) for _ in range(10)
                ]
            ) for _ in range(20)
        ]
        game.add_child(GameObject(children=children))


if utils.should_execute(__name__):
    utils.execute(setup)
