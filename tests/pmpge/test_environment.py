"""
Most of the tests for environment.py are fairly simple as many functions only
provide platform specific values and given that all CI runs are on Python, they
cannot realistically test CircuitPython and MicroPython runs. We therefore delegate
that level of testing to the device specific validation tests that run on the
physical devices.
"""

import pytest

import pmpge.environment as environment
from pmpge.game import Game
from tests.pmpge.test_utilities import with_config_file


def test_is_running_on_desktop():
    """
    Validates that the environment is correctly identified as running on a desktop.
    """
    assert environment.is_running_on_desktop()


def test_is_running_on_microcontroller():
    """
    Validates that the environment is correctly identified as not running on a microcontroller.
    """
    assert not environment.is_running_on_microcontroller()


def test_is_running_on_circuitpython():
    """
    Validates that the environment is correctly identified as not running on CircuitPython.
    """
    assert not environment.is_running_on_circuitpython()


def test_is_running_on_micropython():
    """
    Validates that the environment is correctly identified as not running on MicroPython.
    """
    assert not environment.is_running_on_micropython()


def test_microcontroller_or_desktop():
    """
    Just a simple test to make sure we are not returning a microcontroller and desktop environment
    """
    assert environment.is_running_on_desktop() != environment.is_running_on_microcontroller()


def test_report():
    """
    Simply tests there is no error calling the report method.
    """
    environment.report()


def test_screen_size():
    # Test with no config file, should default to 640x480
    assert environment.screen_size() == (640, 480)

    with_config_file(
        "SCREEN_WIDTH = 800\nSCREEN_HEIGHT = 300\n",
        lambda: environment.screen_size() == (800, 300))

    # Test invalid configuration scenarios.
    with_config_file(
        "SCREEN_WIDTH = 800\n",
        lambda: environment.screen_size(), expect_error=True)

    with_config_file(
        "SCREEN_HEIGHT = 300\n",
        lambda: environment.screen_size(), expect_error=True)


def test_system():
    """
    Validates that the system is the default value which is "pgzero".
    """
    assert environment.system() == "pgzero"


def test_get_controller_driver():
    """
    Checks the default value and an override in the config file.
    """
    assert environment.get_controller_driver() == "pmpge.drivers.controller.pgzero"

    with_config_file(
        'CONTROLLER_DRIVER = "my.controller.driver"\n',
        lambda: environment.get_controller_driver() == "my.controller.driver")


def test_get_device_driver():
    """
    Checks the default value and an override in the config file.
    """
    assert environment.get_device_driver() == "pmpge.drivers.device.none"

    with_config_file(
        'DEVICE_DRIVER = "my.device.driver"\n',
        lambda: environment.get_device_driver() == "my.device.driver")


def test_get_graphics_driver():
    """
    Checks the default value and an override in the config file.
    """
    assert environment.get_graphics_driver() == "pmpge.drivers.graphics.pgzero"

    with_config_file(
        'GRAPHICS_DRIVER = "my.graphics.driver"\n',
        lambda: environment.get_graphics_driver() == "my.graphics.driver")


def test_get_sound_driver():
    """
    Checks the default value and an override in the config file.
    """
    assert environment.get_sound_driver() == "pmpge.drivers.sound.pgzero"

    with_config_file(
        'SOUND_DRIVER = "my.sound.driver"\n',
        lambda: environment.get_sound_driver() == "my.sound.driver")


def test_get_driver():
    """
    Check that the different types of drivers can be retrieved.
    """
    # Just use the default cases.
    assert environment.get_driver("CONTROLLER") == environment.get_controller_driver()
    assert environment.get_driver("DeViCe") == environment.get_device_driver()
    assert environment.get_driver("graphics") == environment.get_graphics_driver()
    assert environment.get_driver("SOuND") == environment.get_sound_driver()

    # Test an unknown driver raises an error.
    with pytest.raises(ValueError):
        environment.get_driver("unknown")


def test_import_driver():
    """
    Validates that drivers module can be imported without errors.
    """
    controller = environment.import_driver("controller")
    device = environment.import_driver("device")
    graphics = environment.import_driver("graphics")
    sound = environment.import_driver("sound")

    # Test an unknown driver raises an error.
    with pytest.raises(ValueError):
        environment.import_driver("unknown")


def test_execute_and_terminate_on_desktop():
    """
    Validates that terminate() can be called when pygame is running it actually terminates.
    This also tests that the execute() function works too (well as best we can). The
    underlying code that is executed is the relevant execute_on_desktop() and
    termiante_on_desktop() code. This also validates that update() and draw() are called
    on the Game instance.
    """
    update_counter = 0

    def update(dt: float):
        nonlocal update_counter
        update_counter += 1
        if update_counter >= 10:
            environment.terminate()

    draw_counter = 0

    def draw(dt: float):
        nonlocal draw_counter
        draw_counter += 1

    game = Game()
    game.add_update_func(update)
    game.add_draw_func(draw)

    environment.execute(game, 320, 200)

    assert update_counter == 10
    assert draw_counter == 10


def test_config_is_loaded() -> None:
    """
    Validates configuration defaults are loaded as well as the local overrides
    contained in config.py.
    """

    # noinspection PyUnresolvedReferences
    with_config_file(
        'TEST_VALUE = 123.456\nTEST_STRING = "Hello world!"\n',
        lambda: environment.config.TEST_VALUE == 123.456 and
                environment.config.TEST_STRING == "Hello world!")
