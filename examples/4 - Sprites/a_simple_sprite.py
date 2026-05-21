"""
This example demonstrates a Sprite which is a GameObject with both a
position and size. The two Sprites move away from each other.
"""

import time

from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import Velocity

game: Game = Game(160, 120)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


game.add_update_func(terminate)

player = Sprite(
    100, 60,
    Velocity(20, 20),
    DrawImage("player.png"))
game.add_child(player)

alien = Sprite(
    100, 60,
    Velocity(-10, -20),
    DrawImage("alien.png"))
game.add_child(alien)

finish = time.monotonic() + 1
game.run()
