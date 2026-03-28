"""
This example demonstrates using a trait. Like a subclass, a trait can have
any of the 5 special methods and these will be called automatically at the
appropriate points: activated(), deactivated(), draw(), update() and
destroyed(). In addition, a trait can have a 6th method called merge() which
is called after the trait has been merged with the GameObject. Traits are
useful as they allow common behaviours to be added to GameObjects without
subclassing.

A trait can be provided as either an instance (as in this example) or as a
type (see `a_using_trait_type.py`). If an instance is provided, all
properties are copied across to the GameObject (shallow copy).
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import sys
import time
import pgzrun
from pgzge.game import Game
from pgzge.game_object import GameObject
from pgzge.traits.drawing import DrawImage
from pgzge.traits.physics import Velocity
from pgzge.traits.position import Position
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


game_object = GameObject(
    Position(100, 100),
    Velocity(20, 20),
    DrawImage("player.png"))
game.add_child(game_object)

game.add_update_func(terminate)


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


finish = time.monotonic() + 2
pgzrun.go()
