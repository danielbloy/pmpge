import sys

import pygame
from pygame import Surface

width: int
height: int
screen_width: int
screen_height: int

scale_surface: Surface = None

mod = sys.modules['__main__']


def init(w: int, h: int, sw: int, sh: int):
    """
    This sets up the game to run at the desired resolution in a python/pygame zero
    environment. If the games specified width or height is smaller than the provided
    screen dimensions, then the image will be scaled. If the games specified width or
    height is larger than the provided screen dimensions, then the game is scaled
    horizontally, vertically or both.

    This function also injects WIDTH, HEIGHT variables into the main application to
    hook into pygame zero. This will overwrite those values if they are set in the
    main Python file.
    """
    global width, height, screen_width, screen_height, scale_surface

    width, height = w, h
    screen_width, screen_height = sw, sh

    if width > screen_width:
        screen_width = width

    if height > screen_height:
        screen_height = height

    setattr(mod, 'WIDTH', screen_width)
    setattr(mod, 'HEIGHT', screen_height)

    if width < screen_width or height < screen_height:
        scale_surface = pygame.Surface((width, height))


def clear(screen, background_colour: tuple[int, int, int]):
    """
    Clears the screen with the specified background colour.
    """
    screen.fill(background_colour)


def draw(screen):
    """
    Performs any scaling that is required.
    """
    if scale_surface:
        scale_surface.blit(screen.surface, (0, 0))
        pygame.transform.scale(scale_surface, (screen_width, screen_height), screen.surface)
