# TODO: This current implementation is only designed to work with a device with a built-in display.
# See: https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-a-bitmap
# See: https://docs.circuitpython.org/en/latest/shared-bindings/displayio/
# TODO: Current issues:
# * No transparency of images (png files)
# * When starting up the game, and sprites are loading, they are displayed on the screen.
# * 20 sprites gives around 30 fps on an EdgeBadge in the multi-sprite validate test
# * Console displays output on EdgeBadge when games starts up.
import adafruit_imageload
import board

import displayio

display = board.DISPLAY
root = displayio.Group()
display.root_group = root


def clear(screen, bgc: tuple[int, int, int]):
    pass


def draw(screen):
    pass


class ImageLoader:
    """
    Mandatory implementation specific class to load and draw an image. Does nothing.
    """
    width: int
    height: int
    bitmap: displayio.Bitmap
    tile_grid: displayio.TileGrid

    def load(self, image: str):
        """
        Loads the named image resource.
        """
        # TODO: This is only supported for bitmaps but would be faster and smaller in memory
        # bitmap = displayio.OnDiskBitmap(f"/images/{image}")
        # tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

        if hasattr(self, 'bitmap'):
            self.bitmap.deinint()

        bitmap, palette = adafruit_imageload.load(
            f"/images/{image}", bitmap=displayio.Bitmap, palette=displayio.Palette)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

        root.append(tile_grid)

        self.width = bitmap.width
        self.height = bitmap.height
        self.bitmap = bitmap
        self.tile_grid = tile_grid

    def draw(self, surface, pos: tuple[int, int]):
        """
        This doesn't actually draw anything, just moves it. thankfully, pos represents
        the top left corner of the image.
        """
        tile_grid = self.tile_grid
        tile_grid.x = pos[0]
        tile_grid.y = pos[1]
