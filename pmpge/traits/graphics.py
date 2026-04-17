from typing import Any, Callable

from pmpge.game_object import GameObject
from pmpge.graphics import ImageResource
from pmpge.palette import WHITE
from sprite import Bounds


class DrawImage:
    """
    This works without requiring properties.
    See notes on Sprite for rules of positioning an image.
    TODO: Update the documentation
    """
    x: float
    y: float
    bounds: Bounds
    image: ImageResource

    def on_notify(self, width: int, height: int):
        bounds = self.bounds
        bounds.width = width
        bounds.height = height
        if hasattr(self, 'x'):
            bounds.x = self.x
            bounds.y = self.y
        else:
            bounds.x = 0
            bounds.y = 0

    def __init__(self, image: str):
        self.bounds = Bounds()
        self.image = ImageResource(image, self.on_notify)

    def update(self, dt: float):
        self.bounds.x = self.x
        self.bounds.y = self.y

    def draw(self, surface: Any):
        self.image.draw(surface, self.bounds.top_left)


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
