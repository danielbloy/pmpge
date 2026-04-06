# This file sets up some variables that are determined from the environment
# that the code is being executed in to allow various parts of the program
# to selectively run based on what is available to it.
#
# THIS FILE SHOULD NOT IMPORT ANY OTHER FILE IN THE TOOLKIT
#
import importlib.util
import sys

################################################################################
# P L A T F O R M
################################################################################
# Internal properties to determine which platform we are running on.
__is_running_on_microcontroller: bool = False
__is_running_on_circuitpython: bool = False
__is_running_on_micropython: bool = False

# First, check the target environment. This is the recommended way to check for
# CircuitPython and MicroPython, see
#   * https://docs.circuitpython.org/en/latest/docs/library/sys.html#sys.implementation
#   * https://docs.micropython.org/en/latest/library/sys.html#sys.implementation
if sys.implementation.name == "circuitpython":
    __is_running_on_microcontroller = True
    __is_running_on_circuitpython = True
elif sys.implementation.name == "micropython":
    __is_running_on_microcontroller = True
    __is_running_on_micropython = True


def is_running_on_desktop() -> bool:
    """
    Returns whether the code is running on a desktop (Windows, Linux or
    Mac) or not. This will be running a full blown Python environment.
    """
    return not __is_running_on_microcontroller


def is_running_on_microcontroller() -> bool:
    """
    Returns whether the code is running on a microcontroller or not. This
    will be running on a more limited Python environment.
    """
    return __is_running_on_microcontroller


def is_running_on_circuitpython() -> bool:
    """
    Returns whether the code is running on a CircuitPython or not.
    """
    return __is_running_on_circuitpython


def is_running_on_micropython() -> bool:
    """
    Returns whether the code is running on a MicroPython or not.
    """
    return __is_running_on_micropython


def report():
    """
    Produces a simple report of the environment the code is running in.
    """

    from pmpge.controller import Controller
    controller = Controller()

    print(f'Running on {platform()} with a {controller.button_count} button controller.')
    del controller


def platform() -> str:
    """
    Returns the supported platform which is used to determine which drivers to
    load and provide the Hardware Abstraction Layer. There are only three valid
    values: Python, CircuitPython and MicroPython.
    """
    if is_running_on_desktop():
        return "Python"

    if is_running_on_circuitpython():
        return "CircuitPython"

    if is_running_on_micropython():
        return "MicroPython"

    raise ValueError("Unsupported platform")


def get_controller_driver() -> str:
    """
    Returns the controller driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the platform we are executing
    within.
    """
    if 'CONTROLLER_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return CONTROLLER_DRIVER

    return f"pmpge.drivers.controller.{platform().lower()}"


def get_device_driver() -> str:
    """
    Returns the device driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the platform we are executing
    within.
    """
    if 'CONTROLLER_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return CONTROLLER_DRIVER

    return f"pmpge.drivers.device.{platform().lower()}_reference"


def get_graphics_driver() -> str:
    """
    Returns the graphics driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the platform we are executing
    within.
    """
    if 'GRAPHICS_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return GRAPHICS_DRIVER

    return f"pmpge.drivers.graphics.{platform().lower()}"


def get_sound_driver() -> str:
    """
    Returns the sound driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the platform we are executing
    within.
    """
    if 'SOUND_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return SOUND_DRIVER

    return f"pmpge.drivers.sound.{platform().lower()}"


def get_platform_driver() -> str:
    """
    Returns the platform driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the platform we are executing
    within. The platform driver is used to provide platform specific functionality.
    """

    if 'PLATFORM_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return PLATFORM_DRIVER

    return f"pmpge.drivers.platform.{platform().lower()}"


def get_driver(module: str) -> str:
    """
    Returns the specified driver for the given module. Valid modules are:
      * controller
      * device
      * graphics
      * platform
      * sound
    """
    match module.lower():
        case "controller":
            return get_controller_driver()
        case "device":
            return get_device_driver()
        case "graphics":
            return get_graphics_driver()
        case "platform":
            return get_platform_driver()
        case "sound":
            return get_sound_driver()

    raise ValueError("Unknown module")


def import_driver(module: str):
    """
    Returns the specified driver for the given module.
    """
    driver = get_driver(module).lower()
    return importlib.import_module(driver)


# Try loading local device settings as overrides.
try:
    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

except ImportError:
    print("No config file found.")
