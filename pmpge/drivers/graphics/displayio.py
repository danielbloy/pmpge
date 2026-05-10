#
# This graphics driver is functional and has reasonable performance on modest
# hardware such as a Pybadge. Presently it provides enough functionality to
# support the desired background colour and the DrawImage trait.
#
# LIMITATION: DISPLAY
#
# Currently, this driver will only work on controllers with built-in displays
# as the board.DISPLAY variable is used.
#
# LIMITATION: HIERARCHY
#
# There is one notable limitation of this driver versus the Pygame zero driver
# that it is important to be aware of and it is related to how the TileGrid
# instances which are used to contain the graphics are constructed. When the
# game is initialise (init() is called) we traverse the entire hierarchy (all
# active AND inactive GameObjects) and generate the TileGrid instances. These
# are all added to the object Group instance. Because we add them in the order
# that we traverse the hierarchy, the implicit draw order is preserved - even
# with the deactivated objects. We also only generate the TileGrid instances
# we need. See the note below about why we don't minic the hierarchy structure.
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
# Destroyed objects always get removed correctly. Deactivated objects get correctly
# hidden.
#
# Why don't we mimic the hierarchy structure?
# Some GameObjects can have multiple TileGrid instances and some GameObjects will
# have none. We could in theory place a single Group instance on each GameObject
# in the hierarchy and attach the TileGrids to those and connect up the Groups in
# the hierarchy. Whilst a definitie potential improvement, it does come with an
# extra memory requirement and unfortunately doesn't address all issues. This is
# because under normal operation the draw() function only cycles over enabled
# objects so if a mix of disabled and enabled objects are added then the draw order
# won't be correct. therefore, the lower memory cost and faster performance option
# was taken.
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

# noinspection PyUnresolvedReferences,PyPackageRequirements
import adafruit_imageload
# noinspection PyUnresolvedReferences,PyPackageRequirements
import board

# noinspection PyUnresolvedReferences,PyPackageRequirements
from displayio import Group, Palette, Bitmap, TileGrid
from pmpge.environment import calculate_scaling_factor
from pmpge.game import Game
from pmpge.game_object import GameObject, draw_hierarchy, traverse_hierarchy

display = board.DISPLAY
display.root_group = None
display.brightness = 0.0  # Turn the display off until the game starts

game: Game | None = None

# Root group to place all items to draw.
root = Group()
background_group: Group = Group()
object_group: Group = Group()
border_group: Group = Group()
root.append(background_group)
root.append(object_group)
root.append(border_group)

# Create a single colour bitmap for the background.
# Source: https://learn.adafruit.com/circuitpython-display-support-using-displayio/draw-pixels
palette = Palette(1)
palette[0] = 0x000000
background = TileGrid(Bitmap(display.width, display.height, 1), pixel_shader=palette)
background_group.append(background)

border_palette = Palette(1)
border_palette[0] = 0x000000


def init(g: Game, sw: int, sh: int, bgc: tuple[int, int, int]):
    """
    Initialises the display by creating the desired background, building the entire
    hierarchy of TileGrids and turning on the display.
    """
    # FUTURE: When the game is smaller than the display and we don't scale, we need to add a border.
    #         The most common is 160 x 120 on a 160 x 128 display.

    global game
    game = g

    # FUTURE: If the background colour is black we could probably avoid the background object
    #         entirely to save RAM.

    # Set the single colour in the palette for our background to the desired background colour
    red = bgc[0] & 255
    green = bgc[1] & 255
    blue = bgc[2] & 255
    palette[0] = red << 16 | green << 8 | blue

    # Here we build the entire graphics hierarchy in order to place the tileGrid
    # instances in the correct order.
    game_object_hierarchy_changed()

    scaling_factor = calculate_scaling_factor(display.width, display.height, g.width, g.height)
    object_group.scale = scaling_factor

    # Now generate the borders to crop the screen to the desired game area. This currently
    # just puts the borders at the bottom of the screen and on the right of the screen.
    # FUTURE: Spread the borders more evenly.
    # TODO: The code to generate the borders could be extract out returning a list of tuples
    #       containing: width, height, x, y
    game_area_width = g.width * scaling_factor
    game_area_height = g.height * scaling_factor
    border_width = display.width - game_area_width
    border_height = display.height - game_area_height

    if border_height > 0:
        bottom_border = TileGrid(Bitmap(display.width, border_height, 1), pixel_shader=border_palette)
        bottom_border.y = game_area_height
        border_group.append(bottom_border)

    if border_width > 0:
        right_border = TileGrid(Bitmap(border_width, display.height, 1), pixel_shader=border_palette)
        right_border.x = game_area_width
        border_group.append(right_border)

    display.root_group = root
    display.brightness = 1


def deinit():
    """
    Removes everything left from the object group.
    """
    global game
    game = None

    # Remove all the items from the object group (most should
    # have been removed via the GameObject.destroy() method.
    display.root_group = None
    while len(object_group) > 0:
        object_group.pop()

    # Now remove the borders.
    while len(border_group) > 0:
        border = border_group.pop()
        border.bitmap.deinit()

    clear_image_cache()


def draw(screen):
    """
    We have to process the entire hierarchy to ensure visbility is set.
    """
    draw_hierarchy(game.root, screen, draw_only_visible=False)
    game.draw(screen)


# This global setting is used to force all GameObjects to re-add their displayio
# objects back to the object Group. This is used when rebuilding the hierarchy.
force_add_tile_grids = False


def game_object_hierarchy_changed():
    """
    This notifies us that the game has made changes to the GameObject hierarchy. We don't
    know what those changes are so we forcibly remove and re-add all displayio objects
    to the object Group. This ensures that the draw order of the objects is correct.

    This is an expensive operation so use sparingly.
    """
    global force_add_tile_grids
    force_add_tile_grids = True

    while len(object_group) > 0:
        object_group.pop()

    def forced_draw(go: GameObject, state):
        go._draw(None)
        return True, None

    traverse_hierarchy(game.root, forced_draw)
    force_add_tile_grids = False


# FUTURE: Do something better for caching. We could also extract out the code in deinit().
image_cache: dict[str, tuple[Bitmap, Palette]] = {}


def clear_image_cache():
    """
    Erases all cached images.
    """
    for bitmap, _ in image_cache.values():
        bitmap.deinit()
    image_cache.clear()


# This extraction has a massive positive impact on draw speed
def load_image(image: str) -> tuple[Bitmap, Palette]:
    """
    This will populate the image_cache with the specified image resource if it
    does not already exist in the cache. It will then return the cached image.
    """
    if image in image_cache:
        image = image_cache[image]
        return image[0], image[1]

    bitmap, palette = adafruit_imageload.load(f"/images/{image}", bitmap=Bitmap, palette=Palette)
    image_cache[image] = bitmap, palette

    # PERFORMANCE: This has a pretty harsh impact on fps, dropping EdgeBadge from 40 to 29 fps
    palette.make_transparent(0)

    return bitmap, palette


class DriverImageResource:
    """
    Implementation specific class to load an image resource. The only mandatory
    method is load(). This class is designed to be combined with `ImageResource`.
    """
    tile_grid: TileGrid
    new_image_loaded: bool  # Set to True when load is called.

    def load(self, image: str) -> tuple[int, int]:
        """
        Loads the named image resource, returning the width and height.
        """
        bitmap, palette = load_image(image)

        # Create a TileGrid to hold the bitmap
        tile_grid = TileGrid(bitmap, pixel_shader=palette)
        tile_grid.hidden = True
        self.new_image_loaded = True

        # Now set the properties on the containing object
        self.tile_grid = tile_grid
        return bitmap.width, bitmap.height


class GraphicsDrawImageTrait:
    """
    This class is designed to be combined with a `DrawImage` trait.
    """
    x: int
    y: int
    _active: bool  # From GameObject
    visible: bool  # From GameObject

    image: DriverImageResource

    def draw(self, surface):
        """
        Draws the image at the specified position, offset from the GameObjects position.
        """
        image = self.image
        if image.new_image_loaded or force_add_tile_grids:
            object_group.append(image.tile_grid)
            image.new_image_loaded = False

        tile_grid = image.tile_grid
        tile_grid.hidden = not (self._active and self.visible)
        tile_grid.x = int(self.x - image.offset_x)
        tile_grid.y = int(self.y - image.offset_y)

    def deactivated(self):
        """
        We just set `hidden` on the TileGrid to stop it being displayed.
        """
        self.image.tile_grid.hidden = True

    def destroyed(self):
        """
        We hide the TileGrid and then remove it from the object group.
        """
        tile_grid = self.image.tile_grid
        tile_grid.hidden = True

        # Only remove from object group if it has previously been attached.
        if not self.image.new_image_loaded:
            object_group.remove(tile_grid)
