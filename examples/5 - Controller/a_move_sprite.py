"""
This example demonstrates a Sprite being moved using the controller
and staying inside the bounds.
"""

import time

from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.controller import MoveWithController
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import Acceleration, Velocity
from pmpge.traits.position import StayInBounds

game: Game = Game(160, 120, (255, 255, 255))


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


controller = Controller()
player = Sprite(
    100, 60,
    Velocity(0, 0),
    Acceleration(0, 50),
    DrawImage("player.png"),
    MoveWithController(50, 0, controller),
    StayInBounds(8, 8, game.width - 8, game.height - 8))
game.add_child(player)

# TODO: Add jump when the controller action button is pressed.

game.add_update_func(terminate)

finish = time.monotonic() + 5
game.run()
