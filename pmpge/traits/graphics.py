from pmpge.graphics import ImageResource, GraphicsDrawImage


class DrawImage(GraphicsDrawImage):
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
    # TODO: Need a generic observable property that notifies when changed.
    image: ImageResource

    def __init__(self, image: str, centered=True):
        image = ImageResource(image)
        image.centered = centered
        self.width = image.width
        self.height = image.height

        if centered:
            image.offset_x = image.width // 2
            image.offset_y = image.height // 2
        else:
            image.offset_x = 0
            image.offset_y = 0

        self.image = image

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
