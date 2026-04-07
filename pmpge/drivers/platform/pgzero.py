import sys

import pgzrun
import pygame

import pmpge.environment as environment

mod = sys.modules['__main__']

# Load the screen width and height from the configuration file, defaulting
# to 640 x 480 if no values are specified. This can be changed/overridden
# by the game.
screen_width: int = 640
screen_height: int = 480

if hasattr(environment, 'WIDTH'):
    screen_width = environment.WIDTH

if hasattr(environment, 'HEIGHT'):
    screen_height = environment.HEIGHT

# The width and height of the game area. This will be equal to or a multiple
# of the screen_width and screen_height.
game_width: int = 0
game_height: int = 0

# This determines the ratio of screen_width/game_width and screen_height/game_height.
game_scale: int = 1
if hasattr(environment, 'SCALE'):
    game_scale = environment.SCALE

game_width = screen_width // game_scale
game_height = screen_height // game_scale


def initialise(width: int | None = None, height: int | None = None) -> tuple[int, int]:
    """
    # TODO: Document this function.
    # TODO: See if we can extract out the pygame specific code.
    Here width and height are the desired width and height of the game.
    """
    global game_width, game_height, screen_width, screen_height

    # If width or height are specified, we recalculate the window.
    if width:
        game_width = width
        screen_width = width * game_scale

    if height:
        game_height = height
        screen_height = height * game_scale

    setattr(mod, 'WIDTH', screen_width)
    setattr(mod, 'HEIGHT', screen_height)

    return game_width, game_height


def execute(game, background_colour: tuple[int, int, int] = None):
    # TODO: Document this function.
    # TODO: Later, experiment if we can extract out common code between Python, CircuitPython and MicroPython
    # TODO: See if we can extract out the pygame zero and pygame specific code.
    # noinspection PyTypeChecker
    screen = None
    scale_surface = None
    if game_scale > 1:
        scale_surface = pygame.Surface((game_width, game_height))

    def draw():
        nonlocal screen
        if not screen:
            screen = getattr(mod, 'screen')

        screen.fill(background_colour)

        game.draw(screen)

        if scale_surface:
            scale_surface.blit(screen.surface, (0, 0))
            pygame.transform.scale(scale_surface, (screen_width, screen_height), screen.surface)

    def update(dt):
        game.update(dt)

    setattr(mod, 'draw', draw)
    setattr(mod, 'update', update)

    pgzrun.go()


def terminate():
    sys.exit(0)
