"""
This example demonstrates a Sprite being moved using the controller
and staying inside the bounds. A simple jump can be performed using
the A button.
"""

import time

from pmpge.controller import Controller
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.sprite import Sprite
from pmpge.traits.controller import MoveWithController, OnPressed
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import Acceleration, Velocity
from pmpge.traits.position import StayInBounds

game: Game = Game(160, 120, (255, 255, 255))


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


game.add_update_func(terminate)


def jump(go: GameObject):
    if go.vy >= 0:
        go.vy = -60


controller = Controller()
player = Sprite(
    100, 60,
    Velocity(0, 0),
    Acceleration(0, 120),
    DrawImage("player.png"),
    MoveWithController(60, 0, controller),
    OnPressed(controller, controller.BUTTON_A, jump),
    StayInBounds(8, 8, game.width - 8, game.height - 8))
game.add_child(player)

finish = time.monotonic() + 5
game.run()
