import pmpge.utilities as utilities
from pmpge.utilities import calculate_scaling_factor


def test_scaling_factor_when_display_too_small():
    """
    Straight forward validate when the display is too small either horizontally or vertically.
    """
    assert calculate_scaling_factor(160, 120, 200, 200) == 1
    assert calculate_scaling_factor(160, 120, 10, 200) == 1
    assert calculate_scaling_factor(160, 120, 200, 10) == 1

    assert calculate_scaling_factor(160, 120, 160, 120) == 1
    assert calculate_scaling_factor(160, 120, 10, 120) == 1
    assert calculate_scaling_factor(160, 120, 160, 10) == 1


def test_scaling_factor():
    """
    Further straightforward tests.
    """
    # Not quite big enough to scale in either direction.
    assert calculate_scaling_factor(160, 120, 81, 61) == 1

    # Not quite big enough to scale either horizontally or vertically
    assert calculate_scaling_factor(160, 120, 10, 61) == 1
    assert calculate_scaling_factor(160, 120, 81, 10) == 1

    # Can scale evenly in both directions
    assert calculate_scaling_factor(160, 120, 80, 60) == 2
    assert calculate_scaling_factor(160, 120, 40, 30) == 4

    # Can scale more in 1 direction than the other
    assert calculate_scaling_factor(160, 120, 40, 60) == 2
    assert calculate_scaling_factor(160, 120, 80, 30) == 2


def test_scaling_factor_with_config_property():
    """
    Regardless of the calculated scaling factor, we always return the configuration scaling factor.
    """

    utilities.config.GRAPHICS_SCALING = 3
    # Would be a calculated scaling factor of 1
    assert calculate_scaling_factor(160, 120, 160, 120) == 3

    # Would be a calculated scaling factor of 2
    assert calculate_scaling_factor(160, 120, 80, 60) == 3

    # Would be a calculated scaling factor of 4
    assert calculate_scaling_factor(160, 120, 40, 30) == 3
    del utilities.config.GRAPHICS_SCALING

# TODO: Add tests for generate_borders
# Common screen resolutions
# 160x120 running on
# 160x128
# 240x240
# 320x240
#
# 120x120 running on
# 160x128
# 240x240
# 320x240

# TODO: Add tests for calculate_fps
