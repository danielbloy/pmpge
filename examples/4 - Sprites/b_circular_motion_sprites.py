"""
This example demonstrates sprites orbiting other sprites.
"""
import math
import time

from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import AngularMotion, AngularRelativeToParent

GAME_WIDTH = 320
GAME_HEIGHT = 240

game: Game = Game(GAME_WIDTH, GAME_HEIGHT)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


game.add_update_func(terminate)

# Add the earth sprite which orbits the centre
earth = Sprite(
    0, 0,
    AngularMotion(GAME_WIDTH // 2, GAME_HEIGHT // 2, 80, math.pi / 4),
    DrawImage("earth.png"))
game.add_child(earth)

# Add two moons which orbit earth
moon = Sprite(
    0, 0,
    AngularRelativeToParent(),
    AngularMotion(0, 0, 20, math.pi),
    DrawImage("moon.png"))
earth.add_child(moon)

moon2 = Sprite(
    0, 0,
    AngularRelativeToParent(),
    AngularMotion(0, 0, 40, -math.pi),
    DrawImage("moon.png"))
earth.add_child(moon2)

# Add a third moon which orbits one of the moons.
moon3 = Sprite(
    0, 0,
    AngularRelativeToParent(),
    AngularMotion(0, 0, 10, -math.pi),
    DrawImage("moon.png"))
moon2.add_child(moon3)

finish = time.monotonic() + 5
game.run()
