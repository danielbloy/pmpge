"""
TODO: Text
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import sys
import time
import pgzrun
from pgzge.game import Game
from pgzge.game_object import GameObject
from pgzero.clock import Clock
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen

game: Game = Game()
clock: Clock
keyboard: Keyboard
screen: Screen

WIDTH = 600
HEIGHT = 700

RED = (255, 0, 0)


def terminate(dt: float):
    if time.monotonic() > finish:
        game.root.destroy()
        sys.exit(0)


class BlinkOneUp:
    def __init__(self):
        self.draw_one_up = True
        self.one_up_transition = 0

    def activated(self):
        self.draw_one_up = True
        self.one_up_transition = time.time() + 0.5

    def draw(self, surface):
        if self.draw_one_up:
            screen.draw.text("1UP", topleft=(20, 0), color=RED, fontsize=36)

    def update(self, dt):
        now = time.time()
        if self.one_up_transition < now:
            self.one_up_transition = now + 0.5
            self.draw_one_up = not self.draw_one_up


trait = BlinkOneUp()
game_object = GameObject(trait)
game.add_child(game_object)

game.add_update_func(terminate)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 2
pgzrun.go()
