"""
This example demonstrates a Sprite which is a GameObject with both a
position and size. The two Sprites move away from each other.
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import time

from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.sprites import SpriteImage
from pmpge.traits.physics import Velocity

game: Game = Game(320, 240)

RED = (255, 0, 0)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


player = Sprite(
    100, 100,
    Velocity(20, 20),
    SpriteImage("player.png"))
game.add_child(player)

alien = Sprite(
    100, 100,
    Velocity(-10, -20),
    SpriteImage("alien.png"))
game.add_child(alien)

game.add_update_func(terminate)

finish = time.monotonic() + 1
game.run()
