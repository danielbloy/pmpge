#
# NOTE: This driver is very much a work in progress and has not yet been optimised and only
#       provides a subset of the required functionality. It is suitable to run the examples
#       and on-device validation tests only. Use with caution.
#
# The code below is marked up with the following tags to indicate where further work is
# required:
#
# * LIMITATION
# * PERFORMANCE
# * ISSUE
# * FUTURE
#
# PERFORMANCE
#
# * 20 sprites gives around 29 fps on an EdgeBadge in the multi-sprite validate test with:
#      SAMPLE_FREQUENCY = 1
#      REPORT_FREQUENCY = 1
#
# * Using transparency is expensive and removing it increases the above test to 40 fps
#
# * Doing manual refreshing seems to seriously hurt performance. It is however worth investigating
#   further when we have a fully working driver to see if we can get smoother updates.
#
# REFERENCES
#
# * https://docs.circuitpython.org/en/latest/shared-bindings/displayio/
# * https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-a-bitmap
# * https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/overview
#
# NOTES
#
# * The display variable is a BusDisplay:
#   See: https://docs.circuitpython.org/en/latest/shared-bindings/busdisplay/index.html#module-busdisplay
#
# * Experiment with visibility of the objects. Group.visible is probably what is needed here.
#   See: https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.Group
#
# * The Z-order of objects is not actually honoured and currently controlled by the order the
#   GameObjects are created. We need to mimic the GameObject hierarchy in Groups/TileGrids.
#
# * Investigate supporting different bitmap types:
#   See: https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics
#

# noinspection PyUnresolvedReferences
import adafruit_imageload
# noinspection PyUnresolvedReferences,PyPackageRequirements
import board

# noinspection PyUnresolvedReferences,PyPackageRequirements
from displayio import Group, Palette, Bitmap, TileGrid

# LIMITATION: Using board.DISPLAY will fail if the device does not have a built-in display.
display = board.DISPLAY
display.refresh(target_frames_per_second=30)
display.brightness = 0.0  # Turn the display off until the game starts

# Create a root group to place all items to draw.
root = Group()

# Create a single colour bitmap for the background.
# Source: https://learn.adafruit.com/circuitpython-display-support-using-displayio/draw-pixels
palette = Palette(1)
palette[0] = 0x000000
background = TileGrid(Bitmap(display.width, display.height, 1), pixel_shader=palette)
root.append(background)


# FUTURE: If we use a tilmemap at a later point, we can probably remove the need for the background layer.


def init(w: int, h: int, sw: int, sh: int, bgc: tuple[int, int, int]):
    # FUTURE: We need to sort out scaling at some point. This can be done by setting: `root.scale = 2`
    #         See: https://learn.adafruit.com/circuitpython-display-support-using-displayio/group#group-scale-3162091

    # Set the single colour in the palette for our background to the desired background colour
    r = bgc[0] & 255
    g = bgc[1] & 255
    b = bgc[2] & 255
    palette[0] = r << 16 | g << 8 | b

    # Setting up the root here stops all the graphics from showing as they are loading.
    display.root_group = root
    display.brightness = 1
    # ISSUE: Adding this statement in stops the console being displayed briefly but negatively impacts framerate
    # display.refresh(target_frames_per_second=30)

    # ISSUE: At this point, the GameObjects will be displayed in the top left corner as they have not
    #        been updated and their initial position is (0, 0). There is no coupling between an
    #        ImageLoader/ImageResource and the corresponding GameObject.


def clear(screen):
    """
    Does not actually need to do anything as displayio handles this for us.
    """
    pass


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
    bitmap: Bitmap
    tile_grid: TileGrid

    def load(self, image: str):
        """
        Loads the named image resource.
        """
        if hasattr(self, 'bitmap'):
            self.bitmap.deinint()

        bitmap, palette = adafruit_imageload.load(f"/images/{image}", bitmap=Bitmap, palette=Palette)

        # PERFORMANCE: This has a pretty harsh impact on fps, dropping EdgeBadge from 40 to 29 fps
        palette.make_transparent(0)

        # Create a TileGrid to hold the bitmap
        tile_grid = TileGrid(bitmap, pixel_shader=palette)
        root.append(tile_grid)

        # Now set the properties on the containing object
        self.width = bitmap.width
        self.height = bitmap.height
        self.bitmap = bitmap
        self.tile_grid = tile_grid

    def draw(self, surface, pos: tuple[int, int]):
        """
        This doesn't actually draw anything, just moves it. The parameter pos represents
        the top left corner of the image so the movement is trivial.
        """
        tile_grid = self.tile_grid
        tile_grid.x = pos[0]
        tile_grid.y = pos[1]
