# TODO: This current implementation is only designed to work with a device with a built-in display.
# See: https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-a-bitmap
# See: https://docs.circuitpython.org/en/latest/shared-bindings/displayio/
# TODO: Current issues:
# * No transparency of images (png files)
# * 20 sprites gives around 40 fps on an EdgeBadge in the multi-sprite validate test with sample turned to minimum
# * Console displays output on EdgeBadge when games starts up.
import adafruit_imageload
import board

import displayio

display = board.DISPLAY
root = displayio.Group()

# Hack for background - this probably needs a better method and more colours:
# Source: https://learn.adafruit.com/circuitpython-display-support-using-displayio/draw-pixels
background_bmp = displayio.Bitmap(display.width, display.height, 1)
palette = displayio.Palette(1)
palette[0] = 0x000000
background = displayio.TileGrid(background_bmp, pixel_shader=palette)
root.append(background)


# TODO: If we use a tilmemap at a later point, we can remove the need for the background layer.

def init(w: int, h: int, sw: int, sh: int):
    # TODO: We need to sort out scaling and drawing at some point.
    # Setting up the root here stops all the graphics from showing as they are loading.
    display.root_group = root


def deinit():
    # TODO: This will clear the display, though in testing we probably don't want to do this.
    # display.root_group = None
    pass


def clear(screen, bgc: tuple[int, int, int]):
    """
    Clears the screen, but actually all it does it reset the background palette
    colour. Strictly, this only needs to happen if the background colour is
    changed so may be a potential future optimisation.
    """
    r = bgc[0] & 255
    g = bgc[1] & 255
    b = bgc[2] & 255
    palette[0] = r << 16 | g << 8 | b


def draw(screen):
    """
    Does not actually need to do anything as displayio handles this for us.
    """
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
        # TODO: This is only supported for bitmaps but would probably be faster and smaller in memory
        # bitmap = displayio.OnDiskBitmap(f"/images/{image}")
        # tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

        if hasattr(self, 'bitmap'):
            self.bitmap.deinint()

        # TODO: Maybe look at some optimisations here.
        bitmap, palette = adafruit_imageload.load(
            f"/images/{image}", bitmap=displayio.Bitmap, palette=displayio.Palette)

        # TODO: This has a pretty harsh impact on fps, dropping EdgeBadge from 40 to 28 fps
        palette.make_transparent(0)

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
