"""
This example demonstrates how to attach an update function to Game. Update
functions are identical in signature to the Pygame Zero update() function
but as many can be attached as you like. They are executed in the order they
are added. In this example, the update function terminates the game after 1
second has elapsed.
"""

import time

from pmpge.game import Game

game: Game = Game()


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


game.add_update_func(terminate)

finish = time.monotonic() + 1
game.run()
