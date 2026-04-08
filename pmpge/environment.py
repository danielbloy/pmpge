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
# Internal properties to determine which system we are running on.
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

    print(f'Running on {system()} with a {controller.button_count} button controller.')
    del controller


def system() -> str:
    """
    Returns the supported system which is used to determine which drivers to
    load and provide the Hardware Abstraction Layer. There are only three valid
    values: pgzero, circuit and micro.
    """
    if is_running_on_desktop():
        return "pgzero"

    if is_running_on_circuitpython():
        return "circuit"

    if is_running_on_micropython():
        return "micro"

    raise ValueError("Unsupported system")


def get_controller_driver() -> str:
    """
    Returns the controller driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the system we are executing
    within.
    """
    if 'CONTROLLER_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return CONTROLLER_DRIVER

    return f"pmpge.drivers.controller.{system().lower()}"


def get_device_driver() -> str:
    """
    Returns the device driver to use. This can be specified in `config.py` to provide
    an override or the `none.py` device driver will be used. This is different from
    the other drivers which have system specific drivers.
    """
    if 'DEVICE_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return DEVICE_DRIVER

    return f"pmpge.drivers.device.none"


def get_graphics_driver() -> str:
    """
    Returns the graphics driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the system we are executing
    within.
    """
    if 'GRAPHICS_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return GRAPHICS_DRIVER

    return f"pmpge.drivers.graphics.{system().lower()}"


def get_sound_driver() -> str:
    """
    Returns the sound driver to use. This can be specified in `config.py` to provide
    an override or a default will be provided depending on the system we are executing
    within.
    """
    if 'SOUND_DRIVER' in globals():
        # noinspection PyUnresolvedReferences
        return SOUND_DRIVER

    return f"pmpge.drivers.sound.{system().lower()}"


def get_driver(module: str) -> str:
    """
    Returns the specified driver for the given module. Valid modules are:
      * controller
      * device
      * graphics
      * sound
    """
    match module.lower():
        case "controller":
            return get_controller_driver()
        case "device":
            return get_device_driver()
        case "graphics":
            return get_graphics_driver()
        case "sound":
            return get_sound_driver()

    raise ValueError("Unknown module")


def import_driver(module: str):
    """
    Returns the specified driver for the given module.
    """
    driver = get_driver(module).lower()
    return importlib.import_module(driver)


def screen_size() -> tuple[int, int]:
    """
    Returns the deafult screen size in pixels. In a Python/pygame zero environment this will
    default to 640 x 480 pixels if not specified in 'config.py'. For a microcontroller this
    will be the physical screen dimensions. In a Python/pygame environment this screen size
    can be overridden.
    """
    width, height = None, None

    if 'SCREEN_WIDTH' in globals():
        # noinspection PyUnresolvedReferences
        width = SCREEN_WIDTH

    if 'SCREEN_HEIGHT' in globals():
        # noinspection PyUnresolvedReferences
        height = SCREEN_HEIGHT

    if (width and not height) or (height and not width):
        raise ValueError(
            "Cannot specify just one of SCREEN_WIDTH or SCREEN_HEIGHT, specify both or neither")

    if width and height:
        # noinspection PyTypeChecker
        return width, height

    if is_running_on_desktop():
        return 640, 480

    raise ValueError("Cannot determine screen size")


def terminate():
    """
    Termiantes the application.
    """
    sys.exit(0)


# Try loading local device settings as overrides.
try:
    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

except ImportError:
    print("No config file found.")

if is_running_on_desktop():
    import pgzrun
    import pygame


def execute(game, game_width: int, game_height: int,
            background_colour: tuple[int, int, int] = None):
    # TODO: Document this function.
    # TODO: Later, experiment if we can extract out common code between Python, CircuitPython and MicroPython
    # TODO: See if we can extract out the pygame zero and pygame specific code.

    screen_width, screen_height = screen_size()

    print(f"Screen width: {game_width}, height: {game_height}")
    print(f"Game width: {game_width}, height: {game_height}")

    # This determines the ratio of screen_width/game_width and screen_height/game_height.
    # game_scale: int = 1
    # if 'SCALE' in globals():
    #    game_scale = SCALE

    # game_width = screen_width // game_scale
    # game_height = screen_height // game_scale

    mod = sys.modules['__main__']

    game_scale = 1

    setattr(mod, 'WIDTH', screen_width)
    setattr(mod, 'HEIGHT', screen_height)

    # noinspection PyTypeChecker
    screen = None
    scale_surface = None
    if game_scale > 1:
        scale_surface = pygame.Surface((game_width, game_height))

    def draw():
        nonlocal screen
        if not screen:
            screen = getattr(mod, 'screen')

        screen.fill(background_colour)

        game.draw(screen)

        if scale_surface:
            scale_surface.blit(screen.surface, (0, 0))
            pygame.transform.scale(scale_surface, (screen_width, screen_height), screen.surface)

    def update(dt):
        game.update(dt)

    setattr(mod, 'draw', draw)
    setattr(mod, 'update', update)

    pgzrun.go()
