from typing import Any

# TODO: Remove dependency on pgzero
from pgzero.loaders import images


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

            self._offset_x = self._surface.get_width() // 2
            self._offset_y = self._surface.get_height() // 2

    def draw(self, surface: Any):
        surface.blit(self._surface, (self.x - self._offset_x, self.y - self._offset_y))

    # TODO: support using x, y as well as centered (anchor)
