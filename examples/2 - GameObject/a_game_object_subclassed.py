"""
This example shows how to subclass from GameObject to add additional custom
behaviour. There are 5 methods that can be overridden, this example just
overrides 3 of them. The 5 methods that can be overridden are: activated(),
deactivated(), draw(), update() and destroyed().
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import sys
import time
import pgzrun
from pgzge.game import Game
from pgzge.game_object import GameObject
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


class BlinkOneUp(GameObject):
    def __init__(self):
        super().__init__()
        self.draw_one_up = True
        self.one_up_transition = 0

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


game_object = BlinkOneUp()
game.add_child(game_object)

game.add_update_func(terminate)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 1
pgzrun.go()
