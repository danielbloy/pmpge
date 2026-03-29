"""
This is a basic template that uses Pygame Zero to drive the game. It doesn't
actually do anything.
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

import pgzrun
from pgzge.game import Game
from pgzero.clock import Clock
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen

game: Game = Game()
clock: Clock
keyboard: Keyboard
screen: Screen

WIDTH = 200
HEIGHT = 200


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


pgzrun.go()
