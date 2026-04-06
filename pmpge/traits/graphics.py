import time
from typing import Any, Callable

# TODO: Remove dependency on pgzero
from pgzero.loaders import images

from pmpge.game_object import GameObject

# TODO: Move colours to Pallette
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)


# TODO: Add size, width, height, topleft, topright etc. properties
# TODO: Add bounding box property


class DrawImage:
    """
    This works without requiring properties.
    """

    # TODO: Test this class
    
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


class DrawAnimatedImage:
    # TODO: This needs implementing properly
    def __init__(self, images: list[str]):
        self.images = images
        self.fps = 2
        self.next_frame = -1
        self.frame = -1

    def activated(self: GameObject):
        self.next_frame = -1
        self.frame = -1

    def draw(self, surface: Any):
        pass

    def update(self, dt: float):
        now = time.time_ns()

        if now > self.next_frame:
            self.frame = (self.frame + 1) % len(self.images)
            self.next_frame = now + (1_000_000_000 / self.fps)


class DrawText:
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

        surface.draw.text(
            text,
            bottomleft=self.pos,
            color=self.colour,
            background=self.background,
            fontname=self.fontname,
            fontsize=self.fontsize)
