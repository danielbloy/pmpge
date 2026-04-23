from typing import Any, Callable

from pgzero.loaders import images

import pmpge.environment as environment


# TODO: This is a temporary solution, the pgzero specific stuff need to be moved out.
class ImageResource:
    """
    Represents an image resource that can be loaded and drawn.
    """

    def __init__(self, image: str, notify: Callable[[int, int], None] = None):
        self.surface = None
        self.notify = notify
        self.load(image)

    @property
    def width(self) -> int:
        """
        The height of the image resource in pixels.
        """
        return self.surface.get_width()

    @property
    def height(self) -> int:
        """
        The width of the image resource in pixels.
        """
        return self.surface.get_height()

    def load(self, image: str):
        """
        Loads the named image resource. This will call the notify method.
        """
        surface = images.load(image)
        self.surface = surface
        notify = self.notify
        if notify:
            notify(surface.get_width(), surface.get_height())

    def draw(self, surface: Any, pos: tuple[float, float]):
        """
        Draws the image, with pos representing the top left corner.
        """
        surface.blit(self.surface, pos)


__graphics = environment.import_driver('graphics')
