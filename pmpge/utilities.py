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


def generate_borders(
        display_width: int, display_height: int, game_width: int, game_height: int, scaling_factor: int) -> list[
    tuple[int, int, int, int]]:
    # Now generate the borders to crop the screen to the desired game area. This currently
    # just puts the borders at the bottom of the screen and on the right of the screen.
    # FUTURE: Spread the borders more evenly.
    # TODO: return x, y of where the game area should start.
    game_area_width = game_width * scaling_factor
    game_area_height = game_height * scaling_factor
    border_width = display_width - game_area_width
    border_height = display_height - game_area_height

    result = []
    if border_height > 0:
        result.append((display_width, border_height, 0, game_area_height))

    if border_width > 0:
        result.append((border_width, display_height, game_area_width, 0))

    return result


# TODO: Implement where is smooths over quarter seconds, always a quarter second behind.
# TODO: Move to a class
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
