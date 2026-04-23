from typing import Any

from pmpge.graphics import ImageResource


class DrawImage:
    """
    DrawImage draws an image at the specified position. By default the image is drawn
    centered on the position (centered according to the same specification as a sprites
    image). Optionally, this can be drawn using the x, y position as the top left corner.

    The DrawImage trait requires a Position trait to be present on the GameObject.
    """
    x: int
    y: int
    width: int
    height: int
    image: ImageResource

    def __init__(self, image: str, centered=True):
        image_resource = ImageResource(image)
        image_resource.centered = centered

        if centered:
            image_resource.offset_x = image_resource.width // 2
            image_resource.offset_y = image_resource.height // 2
        else:
            image_resource.offset_x = 0
            image_resource.offset_y = 0

        self.image = image_resource

    def draw(self, surface: Any):
        """
        Draws the image at the specified position, centered by default.
        """
        self.image.draw(surface, (self.x - self.image.offset_x, self.y - self.image.offset_y))

    def merged(self):
        """
        Hooks the Sprite we have just been attached to into the ImageResource
        notify event to keep the width and height in sync with any new image
        loaded.
        """

        def on_notify(width: int, height: int):
            self.width = width
            self.height = height
            if self.image.centered:
                self.image.offset_x = width // 2
                self.image.offset_y = height // 2
            else:
                self.image.offset_x = 0
                self.image.offset_y = 0

        self.image.notify = on_notify
