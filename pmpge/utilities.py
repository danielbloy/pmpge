# This file contains a range of utility functions used throughout the project.
# Many are extracted from the various drivers to make it easier to test.

################################################################################
# G R A P H I C S    U T I L I T I E S
################################################################################
from pmpge.environment import config


def calculate_scaling_factor(screen_width: int, screen_height: int, game_width: int,
                             game_height: int) -> int:
    """
    TODO: Comments
    """
    if hasattr(config, 'GRAPHICS_SCALING'):
        return config.GRAPHICS_SCALING

    if game_width >= screen_width or game_height >= screen_height:
        return 1

    sx = screen_width // game_width
    sy = screen_height // game_height

    return min(sx, sy)


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
