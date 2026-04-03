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
__is_running_on_linux: bool = False
__is_running_on_mac: bool = False
__is_running_on_windows: bool = False

# First, check the target environment. This is the recommended way to check for
# CircuitPython (see https://docs.circuitpython.org/en/latest/docs/library/sys.html#sys.implementation)
if sys.implementation.name == "circuitpython":
    __is_running_on_microcontroller = True
else:
    # We are not running on CircuitPython so we can assume we are running on
    # a desktop type environment (Windows, Linux or Mac).
    __is_running_on_linux = sys.platform == "linux" or sys.platform == "linux2"
    __is_running_on_mac = sys.platform == "darwin"
    __is_running_on_windows = sys.platform == "win32"


def is_running_on_microcontroller() -> bool:
    """
    Returns whether the code is running on a microcontroller or not.
    """
    return __is_running_on_microcontroller


def is_running_on_desktop() -> bool:
    """
    Returns whether the code is running on a desktop (Windows, Linux or
    Mac) or not.
    """
    return not __is_running_on_microcontroller


def report():
    """
    Produces a simple report of the environment the code is running in.
    """
    running_on = "microcontroller" if is_running_on_microcontroller() else sys.platform

    from pmpge.controller import Controller
    controller = Controller()

    print(f'Running on {running_on} using {hal()} with a {controller.button_count} button controller.')
    del controller


def hal() -> str:
    """
    Returns the supported Hardware Abstraction Layer. this can be manually specified
    in a `config.py` file with a HAL variable. Otherwise it defaults to 'pgzero' in
    a desktop environment and errors otherwise as CircuitPython is not yet supported.
    :return:
    """
    if 'HAL' in globals():
        # noinspection PyUnresolvedReferences
        return HAL

    if is_running_on_desktop():
        return "pgzero"

    raise ValueError("Unsupported HAL.")


def import_hal_module(module: str):
    """
    returns the specified HAL module.
    """
    return importlib.import_module(f"pmpge.hal.{hal()}.{module}")


# TODO: Provide environment information like screen width, height

# Try loading local device settings as overrides.
try:
    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

except ImportError:
    print("No config file found.")
