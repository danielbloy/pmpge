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
# * The deinit() method needs to remove all assets as currently the validation will run out of
#   memory as we do not seem to clear up after ourselves.
#
# * Investigate supporting different bitmap types:
#   See: https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics
#
import gc

# noinspection PyUnresolvedReferences
import adafruit_imageload
# noinspection PyUnresolvedReferences,PyPackageRequirements
import board

# noinspection PyUnresolvedReferences,PyPackageRequirements
from displayio import Group, Palette, Bitmap, TileGrid
from pmpge.game import Game
from pmpge.game_object import draw_hierarchy

game: Game | None = None

# LIMITATION: Using board.DISPLAY will fail if the device does not have a built-in display.
display = board.DISPLAY
display.refresh(target_frames_per_second=30)
display.brightness = 0.0  # Turn the display off until the game starts

# Root group to place all items to draw.
root = Group()

# Create a single colour bitmap for the background.
# Source: https://learn.adafruit.com/circuitpython-display-support-using-displayio/draw-pixels
palette = Palette(1)
palette[0] = 0x000000
background = TileGrid(Bitmap(display.width, display.height, 1), pixel_shader=palette)
root.append(background)  # Needs to be the first item.


# FUTURE: If we use a tilemap at a later point, we can probably remove the need for the background layer.


# TODO: The order that GameObjects are turned into Groups/TileGrid needs to match the hierarchy to
# ensure the draw order is correct. Therefore, we should traverse the entire network at this point
# to create the corresponding structure.
#
# TODO: If the hierarchy changes due to destroyed objects then that is fine as we get an event.
#
# TODO: If the hierarchy changes due to remove_child then the hierarchy needs to be regenerated.
# TODO: How to handle new objects added?


def init(g: Game, sw: int, sh: int, bgc: tuple[int, int, int]):
    # FUTURE: We need to sort out scaling at some point. This can be done by setting: `root.scale = 2`
    #         See: https://learn.adafruit.com/circuitpython-display-support-using-displayio/group#group-scale-3162091
    global game
    game = g

    # Set the single colour in the palette for our background to the desired background colour
    red = bgc[0] & 255
    green = bgc[1] & 255
    blue = bgc[2] & 255
    palette[0] = red << 16 | green << 8 | blue

    # Setting up the root here stops all the graphics from showing as they are loading.
    display.root_group = root
    display.brightness = 1
    # ISSUE: Adding this statement in stops the console being displayed briefly but negatively impacts framerate
    # display.refresh(target_frames_per_second=30)

    # ISSUE: At this point, the GameObjects will be displayed in the top left corner as they have not
    #        been updated and their initial position is (0, 0). There is no coupling between an
    #        ImageLoader/ImageResource and the corresponding GameObject.

    # TODO: Construct initial hierarchy?


def deinit():
    global game, root
    game = None

    display.root_group = None

    root.remove(background)
    del root
    gc.collect()
    root = Group()
    root.append(background)  # Needs to be the first item.

    # Erase all loaded images
    # TODO: see if doing bitmap.deinit() here saves RAM.
    images.clear()


def draw(screen):
    """
    We have to process the entire hierarchy to ensure visbility is set.
    """
    draw_hierarchy(game.root, screen, draw_only_visible=False)
    game.draw(screen)


# FUTURE: Do something better.
images: dict[str, tuple[Bitmap, Palette]] = {}


# This extraction has a massive positive impact on draw speed
def load_image(image: str) -> tuple[Bitmap, Palette]:
    """
    TODO: Comments. Note that it will use the cached version.
    """
    if image in images:
        image = images[image]
        return image[0], image[1]

    bitmap, palette = adafruit_imageload.load(f"/images/{image}", bitmap=Bitmap, palette=Palette)
    images[image] = bitmap, palette

    # PERFORMANCE: This has a pretty harsh impact on fps, dropping EdgeBadge from 40 to 29 fps
    palette.make_transparent(0)

    return bitmap, palette


class DriverImageResource:
    """
    Mandatory implementation specific class to load and draw an image. Does nothing.
    """
    offset_x: int
    offset_y: int
    tile_grid: TileGrid

    # TODO: Need a Group too.

    # TODO: This needs to be combined with a ImageResource trait
    def load(self, image: str) -> tuple[int, int]:
        """
        Loads the named image resource.
        """
        bitmap, palette = load_image(image)

        # Create a TileGrid to hold the bitmap
        tile_grid = TileGrid(bitmap, pixel_shader=palette)
        tile_grid.hidden = True

        root.append(tile_grid)

        # Now set the properties on the containing object
        self.tile_grid = tile_grid
        return bitmap.width, bitmap.height

    # TODO: Render is implementation defined
    # TODO: See if we can move the offset code out
    def render(self, x: int, y: int, visible: bool):
        """
        This moves and sets the visibility of the underlying tile_grid. The parameter pos represents
        the top left corner of the image so the movement is trivial.
        """
        tile_grid = self.tile_grid
        tile_grid.hidden = not visible
        tile_grid.x = int(x - self.offset_x)
        tile_grid.y = int(y - self.offset_y)


class GraphicsDrawImageTrait:
    x: int
    y: int
    active: bool
    visible: bool

    image: DriverImageResource

    # TODO: This needs to be combined with a DrawImage trait
    def draw(self, surface):
        # root.append(self.image.tile_grid)
        self.image.render(self.x, self.y, self.active and self.visible)

    def deactivated(self):
        self.image.tile_grid.hidden = True

    def destroyed(self):
        tile_grid = self.image.tile_grid
        root.remove(tile_grid)
        tile_grid.hidden = True
        del tile_grid
