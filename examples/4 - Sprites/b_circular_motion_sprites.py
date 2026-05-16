"""
This example demonstrates one sprite orbiting another sprite which is
orbiting the centre of the screen.
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

RED = (255, 0, 0)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


earth = Sprite(
    100, 100,
    AngularMotion(GAME_WIDTH // 2, GAME_HEIGHT // 2, 80, math.pi / 4),
    DrawImage("earth.png"))
game.add_child(earth)

moon = Sprite(
    100, 100,
    AngularRelativeToParent(),
    AngularMotion(0, 0, 20, math.pi),
    DrawImage("moon.png"))
earth.add_child(moon)

game.add_update_func(terminate)

finish = time.monotonic() + 5
game.run()
