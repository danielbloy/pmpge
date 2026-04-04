"""
This is a basic template that uses Pygame Zero to drive the game. It doesn't
actually do anything.
"""
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = f'700,100'

from pmpge.game import Game
from pgzero.screen import Screen

screen: Screen
game: Game = Game()


def draw():
    game.draw(screen)


def update(dt):
    game.update(dt)


game.run()
