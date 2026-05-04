def draw(screen):
    """
    Mandatory draw method, does nothing.
    """
    pass


class ImageLoader:
    """
    Mandatory implementation specific class to load and draw an image. Does nothing.
    """
    width: int
    height: int

    def load(self, image: str):
        """
        Loads the named image resource.
        """
        self.width = 0
        self.height = 0

    def draw(self, surface, pos: tuple[int, int]):
        """
        Draws the image, with pos representing the top left corner.
        """
        pass
