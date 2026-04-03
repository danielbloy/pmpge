"""
This example demonstrates using a trait. Like a subclass, a trait can have
any of the 5 special methods and these will be called automatically at the
appropriate points: activated(), deactivated(), draw(), update() and
destroyed(). In addition, a trait can have a 6th method called merge() which
is called after the trait has been merged with the GameObject. Traits are
useful as they allow common behaviours to be added to GameObjects without
subclassing.

A trait can be provided as either a type (as in the first GameObject in
this example) or as an instance. If a type is passed in, it must have
a constructor that takes no argument other than self. If an instance is
provided, all properties are copied across to the GameObject (shallow copy).
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import sys
import time
import pgzrun
from pmpge.game import Game
from pmpge.game_object import GameObject
from pmpge.traits.graphics import DrawImage
from pmpge.traits.physics import Velocity
from pmpge.traits.position import Position
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
    def __init__(self):
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


# Construct a GameObject using a type
game_object = GameObject(BlinkOneUp)
game.add_child(game_object)

# Construct a GameObject using an instance (because it does not have default
# constructor).
game_object_2 = GameObject(
    Position(100, 100),
    Velocity(20, 20),
    DrawImage("player.png"))
game.add_child(game_object_2)

game.add_update_func(terminate)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 1
pgzrun.go()
