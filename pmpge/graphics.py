from typing import Any, Callable

from pgzero.loaders import images

import pmpge.environment as environment


class ImageResource:
    """
    Represents an image resource that can be loaded and drawn.
    """
    surface: Any
    width: int
    height: int
    _name: str
    notify: Callable[[int, int], None] | None

    def __init__(self, name: str, notify: Callable[[int, int], None] = None):
        self.surface = None
        self.width = 0
        self.height = 0
        self._name = name
        self.notify = notify
        self.load(name)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.load(value)

    def load(self, image: str):
        """
        Loads the named image resource. This will call the notify method.
        """
        surface = images.load(image)
        self.surface = surface
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

        notify = self.notify
        if notify:
            notify(surface.get_width(), surface.get_height())

    def draw(self, surface: Any, pos: tuple[float, float]):
        """
        Draws the image, with pos representing the top left corner.
        """
        surface.blit(self.surface, pos)


__graphics = environment.import_driver('graphics')
