from typing import Any

from pmpge.graphics import ImageResource


class SpriteImage:
    """
    This trait displays a static image and uses the size of that image
    to give a Sprite it's width and height.
    """
    width: int
    height: int
    image: ImageResource

    def __init__(self, image: str):
        def on_notify(width: int, height: int):
            self.width = width
            self.height = height

        self.image = ImageResource(image, on_notify)

    # noinspection PyUnresolvedReferences
    def draw(self, surface: Any):
        self.image.draw(surface, self.top_left)
