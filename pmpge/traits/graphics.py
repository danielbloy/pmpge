from typing import Any, Callable

# TODO: Remove dependency on pgzero
from pgzero.loaders import images

from pmpge.game_object import GameObject
from pmpge.palette import WHITE


# TODO: Add size, width, height, topleft, topright etc. properties
# TODO: Add bounding box property


class DrawImage:
    """
    This works without requiring properties.
    See notes on Sprite for rules of positioning an image.
    """

    def __init__(self, image: str):
        self._surface = None
        self._offset_x = None
        self._offset_y = None

        self._image = None
        self.image = image
        self.update(0)

    def update(self, dt: float):
        if self.image != self._image:
            self._image = self.image

            # TODO: need to delegate to the hal resource.
            self._surface = images.load(self.image)

            self._offset_x = self._surface.get_width() / 2
            self._offset_y = self._surface.get_height() / 2

    def draw(self, surface: Any):
        surface.blit(self._surface, (self.x - self._offset_x, self.y - self._offset_y))


class DrawText:

    # TODO: Document this class

    def __init__(self,
                 text: str | Callable[[GameObject], str],
                 colour: tuple[int, int, int] = WHITE,
                 background: tuple[int, int, int] | None = None,
                 fontname: str | None = None,
                 fontsize: int = 16):
        self.text = text
        self.colour = colour
        self.background = background
        self.fontname = fontname
        self.fontsize = fontsize

    def draw(self, surface: Any):
        text = self.text
        if not isinstance(text, str):
            text = self.text(self)

        # TODO: need to delegate to the hal resource.
        surface.draw.text(
            text,
            bottomleft=self.pos,
            color=self.colour,
            background=self.background,
            fontname=self.fontname,
            fontsize=self.fontsize)
