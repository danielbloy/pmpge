"""
This example demonstrates a sprite following a sprite that is orbiting the centre.
"""
import math
import time

from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.graphics import DrawImage
from pmpge.traits.position import AngularMotion, FollowSprite

GAME_WIDTH = 320
GAME_HEIGHT = 240

game: Game = Game(GAME_WIDTH, GAME_HEIGHT)

RED = (255, 0, 0)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.terminate()


# Add the earth sprite which orbits the centre
earth = Sprite(
    0, 0,
    AngularMotion(GAME_WIDTH // 2, GAME_HEIGHT // 2, 80, math.pi / 4),
    DrawImage("earth.png"))
game.add_child(earth)

# Add a moon which follows earth
moon = Sprite(
    GAME_WIDTH // 2, GAME_HEIGHT // 2,
    FollowSprite(earth, 20, 30),
    DrawImage("moon.png"))
game.add_child(moon)

game.add_update_func(terminate)

finish = time.monotonic() + 5
game.run()
