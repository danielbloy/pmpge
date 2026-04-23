from typing import Any

from pmpge.graphics import ImageResource


class DrawImage:
    """
    TODO: Make this work like SpriteImage and use an ImageResource.
    """
    x: int  # TODO: Assumes using x, y but could also allow it to be specified.
    y: int
    width: int
    height: int
    image_resource: ImageResource

    def __init__(self, image: str):
        self._image = image
        self.image = image
        image_resource = ImageResource(image)
        image_resource.offset_x = image_resource.width // 2
        image_resource.offset_y = image_resource.height // 2
        self.image_resource = image_resource

    def update(self, dt: float):
        image = self.image
        if image != self._image:
            self._image = image

            self.image_resource.load(image)

    def draw(self, surface: Any):
        self.image_resource.draw(
            surface, (self.x - self.image_resource.offset_x, self.y - self.image_resource.offset_y))

    def merged(self):
        """
        Hooks the Sprite we have just been attached to into the ImageResource
        notify event to keep the width and height in sync with any new image
        loaded.
        """

        def on_notify(width: int, height: int):
            self.width = width
            self.height = height
            self.image_resource.offset_x = width // 2
            self.image_resource.offset_y = height // 2

        self.image_resource.notify = on_notify

    # TODO: support using x, y as well as centered (anchor)
