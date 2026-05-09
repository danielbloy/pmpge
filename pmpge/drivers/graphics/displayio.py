#
# This graphics driver is functional and has reasonable performance on modest
# hardware such as a Pybadge. Presently it provides enough functionality to
# support the desired background colour and the DrawImage trait.
#
# LIMITATION:
#
# There is one notable limitation of this driver versus the Pygame zero driver
# that it is important to be aware of and it is related to how the TileGrid
# instances which are used to contain the graphics are constructed. When the
# game is initialise (init() is called) we traverse the entire hierarchy and
# generate the TileGrid instances. These are all added to the root Group
# instance. Because we add them in the order that we traverse the hierarchy,
# the implicit Z-order is preserved. We also only generate the TileGrid instances
# we need. Some GameObjects can have multiple TileGrid instances and some
# GameObjects will have none.
#
# However, if the hierarchy later changes, we do not rebuild the order of the
# TileGrid instances. New GameObjects will get added to the end of the list in
# the order they are process. Further, if the parent and child relationships are
# changed for existing objects, the TileGrid order is NOT changed to reflect this.
#
# The way to work around this is straightforward.
#  * Ensure you entire hierarchy is consistent from the start and when adding
#    new branches to the hierarchy, do it in a way that works additively (i.e.
#    add the entire new branch to the Game.root instance).
#  * If you need to rework the hierarchy, call Graphics.game_object_hierarchy_changed()
#    which will force a rebuild of the entire hierarchy. This is expensive so
#    use it sparingly and at points that can accomodate the performance hit.
#
# Destroyed objects always get removed correctly.
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
# * Investigate supporting different bitmap types:
#   See: https://learn.adafruit.com/creating-your-first-tilemap-game-with-circuitpython/indexed-bmp-graphics
#

from gc import collect as gc_collect

# noinspection PyUnresolvedReferences,PyPackageRequirements
import adafruit_imageload
# noinspection PyUnresolvedReferences,PyPackageRequirements
import board

# noinspection PyUnresolvedReferences,PyPackageRequirements
from displayio import Group, Palette, Bitmap, TileGrid
from pmpge.game import Game
from pmpge.game_object import GameObject, draw_hierarchy, traverse_hierarchy

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

    # Here we build the entire graphics hierarchy in order to place the tileGrid
    # instances in the correct order.
    game_object_hierarchy_changed()

    # Setting up the root here stops all the graphics from showing as they are loading.
    display.root_group = root
    display.brightness = 1
    # ISSUE: Adding this statement in stops the console being displayed briefly but negatively impacts framerate
    # display.refresh(target_frames_per_second=30)


def deinit():
    global game, root
    game = None

    display.root_group = None
    root.remove(background)
    del root
    gc_collect()
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


force_rebuild = False


def game_object_hierarchy_changed():
    """
    TODO: Add documentation for this mandatory function which should be called if
    the hierarchy changes. This is a limitation of the displayio driver
    """
    global force_rebuild
    force_rebuild = True

    while len(root) > 0:
        root.pop()

    root.append(background)  # Needs to be the first item.

    def forced_draw(go: GameObject, state):
        go._draw(None)
        return True, None

    traverse_hierarchy(game.root, forced_draw)
    force_rebuild = False


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
    add_to_root: bool

    # TODO: This needs to be combined with a ImageResource trait
    def load(self, image: str) -> tuple[int, int]:
        """
        Loads the named image resource.
        """
        bitmap, palette = load_image(image)

        # Create a TileGrid to hold the bitmap
        tile_grid = TileGrid(bitmap, pixel_shader=palette)
        tile_grid.hidden = True
        self.add_to_root = True

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
        if self.image.add_to_root or force_rebuild:
            root.append(self.image.tile_grid)
            self.image.add_to_root = False

        self.image.render(self.x, self.y, self.active and self.visible)

    def deactivated(self):
        self.image.tile_grid.hidden = True

    def destroyed(self):
        tile_grid = self.image.tile_grid
        tile_grid.hidden = True

        if not self.image.add_to_root:
            root.remove(tile_grid)

        del tile_grid
