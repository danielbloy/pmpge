# This file contains a range of utility functions used throughout the project.
# Many are extracted from the various drivers to make it easier to test.
from pmpge.environment import is_running_on_desktop, RateLimiter
from pmpge.game import Game
from pmpge.game_object import GameObject

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable


################################################################################
# G E N E R A L    U T I L I T I E S
################################################################################


def add_rate_limited_func(thing: Game | GameObject, func: Callable[[float], None], rate: int = 5):
    """
    Adds a rate-limited function to either a Game or GameObject.
    """
    limiter = RateLimiter(func, rate)
    if type(thing) is Game:
        thing.add_update_func(limiter)
    else:
        thing.add_update_handler(lambda _, dt: limiter(dt))


################################################################################
# G R A P H I C S    U T I L I T I E S
################################################################################


def calculate_scaling_factor(display_width: int, display_height: int, game_width: int, game_height: int) -> int:
    """
    Utility function aimed at microcontrollers to help determine the best scaling factor based
    on the passed in display size and game area. If the configuration value GRAPHICS_SCALING
    is specified then that value is returned. Otherwise:
    * If the game area is bigger than the display, the value 1 is returned.
    * Otherwise, return the smallest of the horizontal and vertical scaling factors.
    """
    from pmpge.environment import config

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

    When determining borders, the first 8 pixels go to the bottom border
    (this is the most common and where the status line goes by default).
    The next 8 pixels go to the top border. Each pixel after that is
    alternated bottom, top, bottom, top. Horizontal pixels are shared
    evening with the right hand side getting the first pixel, the left
    hand side the next pixel.

    The common screen resolutions and game areas that we are looking to
    support are:

    * Game areas: (160 x 128), (160 x 120), (120 x 120), (80 x 60)
    * Screen resolutions: (160 x 128), (240, 240), (320 x 240)

    @param display_width: The horizontal resolution of the physical display
    @param display_height: The vertical resolution of the physical display
    @param game_width: The horizontal resolution of the game area (unscaled)
    @param game_height: The vertical resolution of the game area (unscaled)
    @param scaling_factor: The scaling factor to use for the game area. A scaling factor
                           of 2 means each pixel on the game area is scaled to 4 pixels
                           (2 x 2) on the physical display.

    FUTURE: Remove the overlap of the borders.
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

        if border_width < 0 or border_height < 0:
            raise ValueError("The display is not large enough to support the scaled game area")

        if border_height > 0:
            top_height, bottom_height = 0, 0

            # First 8 rows got to the bottom.
            if border_height <= 8:
                bottom_height = border_height
            elif border_height >= 16:
                top_height = border_height // 2
                bottom_height = border_height - top_height
            else:
                bottom_height = 8
                top_height = border_height - 8

            if top_height > 0:
                self.top = (display_width, top_height, 0, 0)

            if bottom_height > 0:
                self.bottom = (display_width, bottom_height, 0, display_height - bottom_height)

        if border_width > 0:
            left_width = border_width // 2
            right_width = border_width - left_width

            if left_width > 0:
                self.left = (left_width, display_height, 0, 0)

            if right_width > 0:
                self.right = (right_width, display_height, display_width - right_width, 0)

        # Adjust the game area starting position
        if self.left:
            self.game_x = self.left[0]

        if self.top:
            self.game_y = self.top[1]

        # Now add the calculated borders to the list to make it easy to iterate.
        for border in [self.left, self.top, self.right, self.bottom]:
            if border:
                self.borders.append(border)


class CalculateFps:
    """
    Class to calculate the FPS over the last 4 intervals to allow a slight smoothing.
    A callback can be provided that will be called at a pre-determined interval (roughly)
    with the most recent calculation for FPS. Do not rely on accuracy of the frequency
    of the callback, it will get called at a maximum of the desired interval.
    """
    interval: float
    quarters: list[int]
    current: int
    index: int
    next_quarter: float

    callback_interval: float
    next_callback: float
    callback: Callable[[int], None] | None

    def __init__(self, interval: float = 0.25, callback_interval: float = 1.0,
                 callback: Callable[[int], None] | None = None):
        self.interval = interval
        self.quarters: list[int] = [0, 0, 0, 0]
        self.current: int = 0
        self.index: int = 0
        self.time_left: float = interval

        self.callback_interval = callback_interval
        self.next_callback = callback_interval
        self.callback = callback

    def update(self, delta_time: float) -> int:
        """
        Call to update the FPS counter. The returned value is the FPS over the last 4
        intervals to allow a slight smoothing.
        """
        self.current += 1
        time_left = self.time_left
        time_left -= delta_time

        if time_left < 0:
            index = self.index
            self.quarters[index] = self.current
            self.current = 0
            time_left += self.interval
            index = (index + 1) % 4
            self.index = index

        self.time_left = time_left

        fps = sum(self.quarters)

        # Now check for callback
        callback = self.callback
        if callback is not None:
            next_callback = self.next_callback
            next_callback -= delta_time
            if next_callback <= 0:
                callback(fps)
                next_callback = self.callback_interval

            self.next_callback = next_callback

        return fps

    def reset(self):
        """
        Simple straightforward reset of the FPS counter.
        """
        self.next_callback = self.callback_interval
        self.index = 0
        self.current = 0
        quarters = self.quarters
        quarters[0] = 0
        quarters[1] = 0
        quarters[2] = 0
        quarters[3] = 0
