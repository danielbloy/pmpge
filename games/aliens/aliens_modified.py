# This version of aliens uses a mix of subclasses and using the GameObject events.
# Original source material: https://codeclubadventures.co.uk/python/pygame/aliens/
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import pgzrun
from pgzge.core import Game
from pgzero.clock import Clock
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen

clock: Clock
keyboard: Keyboard
screen: Screen
pgzge: Game = Game()

WIDTH = 600
HEIGHT = 700

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)


def draw():
    pgzge.draw(screen.surface)


def update(dt):
    pgzge.update(dt)


pgzrun.go()
