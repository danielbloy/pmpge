import pmpge.utilities as utilities
from pmpge.utilities import calculate_scaling_factor, Borders


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


def validate_borders(
        display_width: int, display_height: int, game_width: int, game_height,
        left_width: int, right_width: int, top_height: int, bottom_height: int):
    borders = Borders(display_width, display_height, game_width, game_height, 1)

    expected_number_of_borders = 4
    print(f"Display: {display_width} x {display_height}: Game: {game_width} x {game_height}")
    print(f"Left: {left_width}, Right: {right_width}, Top: {top_height}, Bottom: {bottom_height}")
    print(borders.borders)

    if left_width == 0:
        assert borders.left is None
        expected_number_of_borders -= 1
    else:
        assert borders.left[0] == left_width  # Width
        assert borders.left[1] == display_height  # Height
        assert borders.left[2] == 0  # x
        assert borders.left[3] == 0  # y

    if right_width == 0:
        assert borders.right is None
        expected_number_of_borders -= 1
    else:
        assert borders.right[0] == right_width  # Width
        assert borders.right[1] == display_height  # Height
        assert borders.right[2] == display_width - right_width  # x
        assert borders.right[3] == 0  # y

    if top_height == 0:
        assert borders.top is None
        expected_number_of_borders -= 1
    else:
        assert borders.top[0] == display_width  # Width
        assert borders.top[1] == top_height  # Height
        assert borders.top[2] == 0  # x
        assert borders.top[3] == 0  # y

    if bottom_height == 0:
        assert borders.bottom is None
        expected_number_of_borders -= 1
    else:
        assert borders.bottom[0] == display_width  # Width
        assert borders.bottom[1] == bottom_height  # Height
        assert borders.bottom[2] == 0  # x
        assert borders.bottom[3] == display_height - bottom_height  # y

    assert len(borders.borders) == expected_number_of_borders


def test_borders_just_top_and_bottom():
    """
    The first 8 pixels are always given to the bottom border.
    The next 8 pixels are always given to the top border.
    After that, the pixels are shared bottom, top in an alternating fashion.
    """

    def validate_border(game_height: int, top_height: int, bottom_height: int):
        validate_borders(160, 128, 160, game_height, 0, 0, top_height, bottom_height)

    # Just bottom
    validate_border(128, 0, 0)
    validate_border(127, 0, 1)
    validate_border(126, 0, 2)
    validate_border(125, 0, 3)
    validate_border(124, 0, 4)
    validate_border(123, 0, 5)
    validate_border(122, 0, 6)
    validate_border(121, 0, 7)
    validate_border(120, 0, 8)

    # Just top
    validate_border(119, 1, 8)
    validate_border(118, 2, 8)
    validate_border(117, 3, 8)
    validate_border(116, 4, 8)
    validate_border(115, 5, 8)
    validate_border(114, 6, 8)
    validate_border(113, 7, 8)
    validate_border(112, 8, 8)

    # Now share
    validate_border(111, 8, 9)
    validate_border(110, 9, 9)
    validate_border(109, 9, 10)
    validate_border(108, 10, 10)
    validate_border(107, 10, 11)


def test_borders_just_left_and_right():
    """
    These are shared evenly between left and right borders
    """

    def validate_border(game_width: int, left_width: int, right_width: int):
        validate_borders(160, 128, game_width, 128, left_width, right_width, 0, 0)

    validate_border(160, 0, 0)
    validate_border(159, 0, 1)
    validate_border(158, 1, 1)
    validate_border(157, 1, 2)
    validate_border(156, 2, 2)
    validate_border(155, 2, 3)
    validate_border(154, 3, 3)
    validate_border(153, 3, 4)


def test_borders_top_bottom_and_left_right():
    """
    Test all four borders.
    """

    def validate_border(
            game_width: int, game_height, left_width: int, right_width: int, top_height: int, bottom_height: int):
        validate_borders(160, 128, game_width, game_height, left_width, right_width, top_height, bottom_height)

    validate_border(160, 128, 0, 0, 0, 0)
    validate_border(159, 127, 0, 1, 0, 1)
    validate_border(158, 126, 1, 1, 0, 2)
    validate_border(157, 125, 1, 2, 0, 3)
    validate_border(156, 124, 2, 2, 0, 4)
    validate_border(155, 123, 2, 3, 0, 5)
    validate_border(154, 122, 3, 3, 0, 6)
    validate_border(153, 121, 3, 4, 0, 7)
    validate_border(152, 120, 4, 4, 0, 8)
    validate_border(151, 119, 4, 5, 1, 8)
    validate_border(150, 118, 5, 5, 2, 8)
    validate_border(149, 117, 5, 6, 3, 8)
    validate_border(148, 116, 6, 6, 4, 8)
    validate_border(147, 115, 6, 7, 5, 8)
    validate_border(146, 114, 7, 7, 6, 8)
    validate_border(145, 113, 7, 8, 7, 8)
    validate_border(144, 112, 8, 8, 8, 8)
    validate_border(143, 111, 8, 9, 8, 9)
    validate_border(142, 110, 9, 9, 9, 9)
    validate_border(141, 109, 9, 10, 9, 10)
    validate_border(140, 108, 10, 10, 10, 10)


def test_borders_with_scaling_factor():
    """

    """
    assert False


def test_borders_common_size():
    """
    This tests the most common size of screens that we expect to encounter.
    """
    validate_borders(160, 128, 160, 128, 0, 0, 0, 0)
    validate_borders(160, 128, 160, 120, 0, 0, 0, 8)
    validate_borders(160, 128, 120, 120, 20, 20, 0, 8)
    validate_borders(160, 128, 80, 60, 40, 40, 34, 34)

    validate_borders(240, 240, 160, 128, 40, 40, 56, 56)
    validate_borders(240, 240, 160, 120, 40, 40, 60, 60)
    validate_borders(240, 240, 120, 120, 60, 60, 60, 60)
    validate_borders(240, 240, 80, 60, 80, 80, 90, 90)

    validate_borders(320, 240, 160, 128, 80, 80, 56, 56)
    validate_borders(320, 240, 160, 120, 80, 80, 60, 60)
    validate_borders(320, 240, 120, 120, 100, 100, 60, 60)
    validate_borders(320, 240, 80, 60, 120, 120, 90, 90)

# TODO: Add tests for calculate_fps
