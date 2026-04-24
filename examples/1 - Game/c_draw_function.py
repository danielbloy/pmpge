"""
This example demonstrates two update functions and a single draw function
being attached to Game. Draw functions take a single argument that is
nominally called surface but can represent any object. Just like update
functions, multiple draw functions can be added to a Game instance and
they are called in the order added.

In this example, we blit to the surface the player image which is moved by
the update_image function.
"""

import time

from pmpge.game import Game

game: Game = Game()


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


pos = (100, 200)
velocity = (50, 50)


def update_image(dt: float):
    global pos
    pos = (pos[0] + (velocity[0] * dt), pos[1] + (velocity[1] * dt))


def draw_image(surface):
    surface.blit('player', pos)


game.add_update_func(terminate)
game.add_update_func(update_image)
game.add_draw_func(draw_image)

finish = time.monotonic() + 1
game.run()
