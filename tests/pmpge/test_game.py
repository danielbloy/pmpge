import pytest

from pmpge.game import Game
from tests.pmpge.test_utilities import with_config_file


def test_empty_constructor():
    """
    Validates that a Game object can be created with an empty constructor and work.
    """
    game = Game()
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (0, 0, 0)
    assert game.root
    assert len(game.children) == 0


def test_constructor_with_width_and_height():
    """
    Validates that both a width and height must be specified for a Game to be created.
    """
    with pytest.raises(ValueError):
        Game(width=100)

    with pytest.raises(ValueError):
        Game(height=100)

    game = Game(width=100, height=100)
    assert game.width == 100
    assert game.height == 100
    assert game.background_color == (0, 0, 0)
    assert game.root
    assert len(game.children) == 0


def test_constructor_with_config():
    """
    Validates that the configuration is used when width and height are not specified.
    """

    def validate():
        # Using the default configuration from the config file.
        game = Game()
        assert game.width == 800
        assert game.height == 300

        # Override the default configuration from the config file.
        game = Game(width=320, height=240)
        assert game.width == 320
        assert game.height == 240

        return True

    with_config_file(
        "SCREEN_WIDTH = 800\nSCREEN_HEIGHT = 300\n", validate)


def test_constructor_with_background_colour():
    """
    Validates that a Game can be created with a custom background colour.
    """
    game = Game()
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (0, 0, 0)
    assert game.root
    assert len(game.children) == 0

    game = Game(background_color=(1, 2, 3))
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (1, 2, 3)
    assert game.root
    assert len(game.children) == 0

    game = Game(background_color=(6, 5, 4))
    assert game.width == 640
    assert game.height == 480
    assert game.background_color == (6, 5, 4)
    assert game.root
    assert len(game.children) == 0

# TODO: Test add an removing children from root
# TODO: Test adding draw and update functions
# TODO: Validate the order that draw and update functions are called after  the hierarchy.
# TODO: Validate terminate
# TODO: Validate run
