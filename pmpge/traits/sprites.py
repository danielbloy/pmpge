from typing import Any

from pmpge.graphics import ImageResource


class SpriteImage:
    """
    This trait displays a static image and uses the size of that image
    to give a Sprite it's width and height.
    """
    width: int
    height: int
    top_left: tuple[int, int]
    image: ImageResource

    def __init__(self, name: str):
        """
        Initialises the image and sets the width and height manually.
        This does not use the notify callback for setting the width and height
        as this trait is designed to work with a Sprite and therefore is
        expected to be merged. We hook into the notify event in merged().
        """
        image = ImageResource(name)
        self.image = image
        self.width = image.width
        self.height = image.height

    def draw(self, surface: Any):
        """
        Uses the Sprites bounds to draw the image. The Sprite will provide the
        `top_left` property.
        """
        self.image.draw(surface, self.top_left)

    def merged(self):
        """
        Hooks the Sprite we have just been attached to into the ImageResource
        notify event to keep the width and height in sync with any new image
        loaded.
        """

        def on_notify(width: int, height: int):
            self.width = width
            self.height = height

        self.image.notify = on_notify
