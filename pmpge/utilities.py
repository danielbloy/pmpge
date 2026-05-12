# This file contains a range of utility functions used throughout the project.
# Many are extracted from the various drivers to make it easier to test.

################################################################################
# G R A P H I C S    U T I L I T I E S
################################################################################
from pmpge.environment import config


def calculate_scaling_factor(display_width: int, display_height: int, game_width: int, game_height: int) -> int:
    """
    Utility function aimed at microcontrollers to help determine the best scaling factor based
    on the passed in display size and game area. If the configuration value GRAPHICS_SCALING
    is specified then that value is returned. Otherwise:
    * If the game area is bigger than the display, the value 1 is returned.
    * Otherwise, return the smallest of the horizontal and vertical scaling factors.
    """
    if hasattr(config, 'GRAPHICS_SCALING'):
        return config.GRAPHICS_SCALING

    if game_width >= display_width or game_height >= display_height:
        return 1

    sx = display_width // game_width
    sy = display_height // game_height

    return min(sx, sy)


class Borders:
    """
    This class is used to calculate borders for a microcontroller screen.
    There can be up to 4 borders, one per edge of the screen. Each border
    has a tuple of 4 values to define its size and position:
        * width
        * height
        * x
        * y

    It also calculates the relative position for the game area as it may
    need to be shifted if there is a left or top border.

    The common screen resolutions and game areas that we are looking to
    support are:

    * Game areas: (160 x 128), (160 x 120), (120 x 120), (80 x 60)
    * Screen resolutions: (160 x 128), (240, 240), (320 x 240)

    FUTURE: Remove the overlap of the borders.
    FUTURE: Ensure space for the metrics status bar of 8 pixels.
    """
    borders: list[tuple[int, int, int, int]]
    top: tuple[int, int, int, int] | None
    bottom: tuple[int, int, int, int] | None
    left: tuple[int, int, int, int] | None
    right: tuple[int, int, int, int] | None

    game_x: int
    game_y: int

    def __init__(self, display_width: int, display_height: int, game_width: int, game_height: int, scaling_factor: int):
        self.borders = []
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.game_x = 0
        self.game_y = 0

        game_area_width = game_width * scaling_factor
        game_area_height = game_height * scaling_factor
        border_width = display_width - game_area_width
        border_height = display_height - game_area_height

        if border_height > 0:
            self.right = (display_width, border_height, 0, game_area_height)

        if border_width > 0:
            self.bottom = (border_width, display_height, game_area_width, 0)

        # Adjust the game area starting position
        if self.left:
            self.game_x = self.left[0]

        if self.top:
            self.game_y = self.top[1]

        # Now add the calculated borders to the list to make it easy to iterate.
        for border in [self.left, self.top, self.right, self.bottom]:
            if border:
                self.borders.append(border)


# TODO: Implement where is smooths over quarter seconds, always a quarter second behind.
# TODO: Move to a class
# TODO: Count down to zero through ticks and updates.
fps_last_4_quarters: list[int] = [0, 0, 0, 0]
fps_current_quarter: int
fps_current_quarter_index: int = 0
fps_next_quarter_tick: float = 0


def calculate_fps() -> int:
    """
    TODO: Comments
    """
    global fps_current_quarter
    fps_current_quarter += 1
    return sum(fps_last_4_quarters)
