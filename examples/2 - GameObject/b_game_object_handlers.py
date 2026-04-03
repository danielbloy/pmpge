"""
This example demonstrates a method of adding functionality to a GameObject instance
without subclassing. This is achieved by creating a class that handles the new
functionality. This example is shown for completeness. This is not the recommended
way to add functionality. It is recommended to either subclass or use traits. Those
examples can be seen in `a_game_object_subclassed.py1 and `c_game_object_with_trait.py`.
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import sys
import time
import pgzrun
from pmpge.game import Game
from pmpge.game_object import GameObject
from pgzero.screen import Screen

screen: Screen
game: Game = Game()

WIDTH = 200
HEIGHT = 200

RED = (255, 0, 0)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.root.destroy()
        sys.exit(0)


class BlinkOneUp:
    # The constructor is not actually needed and does not get executed but is included
    # to prevent PyCharm warnings.
    def __init__(self):
        self.draw_one_up = True
        self.one_up_transition = 0

    # This method both creates and initialises the properties on the GameObject. Remember,
    # the __init()__ method is never actually called in the example.
    def activated(self):
        self.draw_one_up = True
        self.one_up_transition = time.time() + 0.5

    def draw(self, surface):
        if self.draw_one_up:
            surface.draw.text("1UP", topleft=(20, 0), color=RED, fontsize=36)

    def update(self, dt):
        now = time.time()
        if self.one_up_transition < now:
            self.one_up_transition = now + 0.5
            self.draw_one_up = not self.draw_one_up


# noinspection PyTypeChecker
game_object = GameObject(
    activate_handler=BlinkOneUp.activated,
    draw_handler=BlinkOneUp.draw,
    update_handler=BlinkOneUp.update)

game.add_child(game_object)

game.add_update_func(terminate)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 1
pgzrun.go()
