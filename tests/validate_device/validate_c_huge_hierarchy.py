"""
Creates a huge hierarchy of GameObjects to see memory usage and
performance impact. This is only designed to run on a Desktop PC
as usually a microcontroller will not have enough RAM and even
if it does have enough RAM, it takes ages to construct the
40,000 GameObjects
"""

import tests.validate_device.utils as utils
from pmpge.game import Game
from pmpge.game_object import GameObject


def setup(game: Game):
    # Short-circuit if running on a microcontroller.
    from pmpge.environment import is_running_on_microcontroller
    if is_running_on_microcontroller():
        print("Skipping creating huge hierarchy of GameObjects on microcontroller")
        return

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
