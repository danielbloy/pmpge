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


class GameHud:
    def activated(self):
        print("run")
        self.draw_one_up = True
        self.one_up_transition = time.time() + 0.5

    def draw(self, surface):
        print("draw")
        if self.draw_one_up:
            screen.draw.text("1UP", topleft=(20, 0), color=RED, fontsize=36)

    def update(self, dt):
        print("update")
        now = time.time()
        if self.one_up_transition < now:
            self.one_up_transition = now + 0.5


game_object = GameObject(
    activate_handler=GameHud.activated,
    draw_handler=GameHud.draw,
    update_handler=GameHud.update)

game.add_child(game_object)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 2
pgzrun.go()
