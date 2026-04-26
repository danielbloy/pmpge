import sys
from typing import Any

import pygame
from pgzero.loaders import images
from pygame import Surface

width: int = 0
height: int = 0
screen_width: int = 0
screen_height: int = 0
background_colour: tuple[int, int, int] = (0, 0, 0)
scale_surface: Surface = None

mod = sys.modules['__main__']


def init(w: int, h: int, sw: int, sh: int, bgc: tuple[int, int, int]):
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
    global width, height, screen_width, screen_height, background_colour, scale_surface

    width, height = w, h
    screen_width, screen_height = sw, sh
    background_colour = bgc

    if width > screen_width:
        screen_width = width

    if height > screen_height:
        screen_height = height

    setattr(mod, 'WIDTH', screen_width)
    setattr(mod, 'HEIGHT', screen_height)

    if width < screen_width or height < screen_height:
        scale_surface = pygame.Surface((width, height))


def clear(screen):
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
        pygame.transform.scale(
            scale_surface,
            (screen_width, screen_height), screen.surface)  # noqa: F821


class ImageLoader:
    """
    Implementation specific class to load and draw an image.
    """
    surface: Any
    width: int
    height: int

    def load(self, image: str):
        """
        Loads the named image resource.
        """
        surface = images.load(image)
        self.surface = surface
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def draw(self, surface: Any, pos: tuple[int, int]):
        """
        Draws the image, with pos representing the top left corner.
        """
        surface.blit(self.surface, pos)
