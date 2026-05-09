from pmpge.graphics import ImageResource, GraphicsDrawImageTrait


class DrawImage(GraphicsDrawImageTrait):
    """
    DrawImage draws an image at the specified position. By default the image is drawn
    centered on the position (centered according to the same specification as a sprites
    image). Optionally, this can be drawn using the x, y position as the top left corner.

    The DrawImage trait requires a Position trait to be present on the GameObject.
    """
    x: int
    y: int

    # The width and height properties are required for Sprites but useful generally
    width: int
    height: int

    image: ImageResource

    # TODO: Centered should be true for sprites
    def __init__(self, image: str, centered: bool = True):
        # FUTURE: We could extract ImageResource to be passed in.
        image = ImageResource(image)

        self.width = image.width
        self.height = image.height
        self.image = image

    def merged(self):
        """
        Hooks the Sprite we have just been attached to into the ImageResource
        notify event to keep the width and height in sync with any new image
        loaded.
        """

        def on_notify():
            width, height = self.image.width, self.image.height
            self.width = width
            self.height = height

        self.image.notify = on_notify

        if self.centered:
            self.offset_x = self.width // 2
            self.offset_y = self.height // 2
        else:
            self.offset_x = 0
            self.offset_y = 0
