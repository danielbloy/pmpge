"""
This example demonstrates how to attach an update function to Game. Update
functions are identical in signature to the Pygame Zero update() function
but as many can be attached as you like. They are executed in the order they
are added. In this example, the update function terminates the game after 2
seconds have elapsed.
"""
import os
import sys

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import time
import pgzrun
from pgzge.game import Game

WIDTH = 600
HEIGHT = 700


def terminate(dt: float):
    if time.monotonic() > finish:
        game.root.destroy()
        sys.exit(0)


game: Game = Game()

game.add_update_func(terminate)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 2
pgzrun.go()
