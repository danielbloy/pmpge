"""
Most of the tests for environment.py are fairly simple as many functions only
provide platform specific values and given that all CI runs are on Python, they
cannot realistically test CircuitPython and MicroPython runs. We therefore delegate
that level of testing to the device specific validation tests that run on the
physical devices.
"""
import os
import pathlib
from collections.abc import Callable
from importlib import reload

import pmpge.environment as environment


def with_config_file(contents: str, test: Callable[[], bool]) -> None:
    """
    Utility function for testing using a custom config file. It cleans up the file after the test.
    """
    config_file = f"{pathlib.Path().resolve()}/config.py"

    try:
        with open(config_file, "w") as file:
            file.write(contents)

        reload(environment)
        assert test()

    finally:
        os.remove(config_file)


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


def test_system():
    """
    Validates that the system is the default value which is "pgzero".
    """
    assert environment.system() == "pgzero"


def test_system():
    """
    Validates that the system is the default value which is "pgzero".
    """
    assert environment.system() == "pgzero"

# TODO: Test the following functions:
#   * get_controller_driver()
#   * get_device_driver()
#   * get_graphics_driver()
#   * get_sound_driver()
#   * screen_size()
#   * system()
#   * termiante()
#   * execute()
