"""
This example demonstrates using a trait. Like a subclass, a trait can have
any of the 5 special methods and these will be called automatically at the
appropriate points: activated(), deactivated(), draw(), update() and
destroyed(). In addition, a trait can have a 6th method called merge() which
is called after the trait has been merged with the GameObject. Traits are
useful as they allow common behaviours to be added to GameObjects without
subclassing.

A trait can be provided as either an instance (as in this example) or as a
type (see `a_using_trait_type.py`). If an instance is provided, all
properties are copied across to the GameObject (shallow copy).
"""

import time

from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position

game: Game = Game(320, 240)

RED = (255, 0, 0)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


game_object = GameObject(
    Position(100, 100),
    Velocity(20, 20),
    DrawImage("player.png"))
game.add_child(game_object)

game.add_update_func(terminate)

finish = time.monotonic() + 1
game.run()
