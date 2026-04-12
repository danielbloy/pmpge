# This file sets up some variables that are determined from the environment
# that the code is being executed in to allow various parts of the program
# to selectively run based on what is available to it.
#
# THIS FILE SHOULD NOT IMPORT ANY OTHER FILE IN THE FRAMEWORK
#
import importlib.util
import sys

################################################################################
# S Y S T E M    P R O P E R T I E S
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

    print(
        f'Running on {system()} with {screen_size()} screen and {controller.button_count} button controller.')
    del controller


def screen_size() -> tuple[int, int]:
    """
    Returns the default screen size in pixels. In a Python/pygame zero environment this will
    default to 640 x 480 pixels if not specified in 'config.py'. For a microcontroller this
    will be the physical screen dimensions. In a Python/pygame environment this screen size
    can be overridden.
    """
    width, height = None, None

    if config and hasattr(config, 'SCREEN_WIDTH'):
        width = config.SCREEN_WIDTH

    if config and hasattr(config, 'SCREEN_HEIGHT'):
        height = config.SCREEN_HEIGHT

    if (width and not height) or (height and not width):
        raise ValueError(
            "Cannot specify just one of SCREEN_WIDTH or SCREEN_HEIGHT, specify both or neither")

    if width and height:
        # noinspection PyTypeChecker
        return width, height

    if is_running_on_desktop():
        return 640, 480

    raise ValueError("Cannot determine screen size")


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


################################################################################
# D R I V E R S
################################################################################

def get_controller_driver() -> str:
    """
    Returns the controller driver to use. This can be specified in `config.py` to provide
    an override, otherwise a default will be provided depending on the system we are executing
    within.
    """
    if config and hasattr(config, 'CONTROLLER_DRIVER'):
        return config.CONTROLLER_DRIVER

    if is_running_on_desktop():
        return "pmpge.drivers.controller.pgzero"

    raise SystemError("Cannot determine controller driver")


def get_device_driver() -> str:
    """
    Returns the device driver to use. This can be specified in `config.py` to provide
    an override, otherwise the `none.py` device driver will be used. This is different
    from the other drivers which have system specific drivers.
    """
    if config and hasattr(config, 'DEVICE_DRIVER'):
        return config.DEVICE_DRIVER

    return "pmpge.drivers.device.none"


def get_graphics_driver() -> str:
    """
    Returns the graphics driver to use. This can be specified in `config.py` to provide
    an override, otherwise a default will be provided depending on the system we are
    executing within.
    """
    if config and hasattr(config, 'GRAPHICS_DRIVER'):
        return config.GRAPHICS_DRIVER

    if is_running_on_desktop():
        return "pmpge.drivers.graphics.pgzero"

    if is_running_on_micropython():
        return "pmpge.drivers.graphics.picographics"

    if is_running_on_circuitpython():
        return "pmpge.drivers.graphics.displayio"

    raise SystemError("Cannot determine graphics driver")


def get_sound_driver() -> str:
    """
    Returns the sound driver to use. This can be specified in `config.py` to provide
    an override, otherwise a default will be provided depending on the system we are
    executing within.
    """
    if config and hasattr(config, 'SOUND_DRIVER'):
        return config.SOUND_DRIVER

    if is_running_on_desktop():
        return "pmpge.drivers.sound.pgzero"

    raise SystemError("Cannot determine sound driver")


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
    driver = get_driver(module)
    return importlib.import_module(driver)


################################################################################
# E X E C U T I O N
################################################################################

__execute: bool = False


def execute_on_microcontroller(game, background_colour: tuple[int, int, int] = None):
    """
    This executes the game at the desired resolution. If the screen display is larger
    than the specified width and height, the application will scale if it is able to
    do so.
    """
    if not background_colour:
        background_colour = (0, 0, 0)

    width, height = game.width, game.height
    screen_width, screen_height = screen_size()

    # On a microcontroller, a larger game size than screen size is an error.
    if width > screen_width or height > screen_height:
        raise ValueError("Game width and height cannot be larger than screen")

    global __execute
    __execute = True

    last = time.monotonic()
    while __execute:
        now = time.monotonic()
        dt = now - last
        last = now
        game.update(dt)
        game.draw(None)


def execute_on_desktop(game, background_colour: tuple[int, int, int] = None):
    """
    This executes the game at the desired resolution in a python/pygame environment. If
    the games specified width or height is smaller than the dimensions provided by
    screen_size() then the image will be scaled. If the games specified width or height
    is larger than the dimensions provided by screen_size() then the game is scaled
    horizontally, vertically or both.

    This function also injects WIDTH, HEIGHT, draw() and update() functions into the
    main application to hook into pygame zero. This will overwrite the those values
    or functions if they are set in the main Python file.
    """
    if not background_colour:
        background_colour = (0, 0, 0)

    width, height = game.width, game.height
    screen_width, screen_height = screen_size()
    
    if is_running_on_desktop():
        if width > screen_width:
            screen_width = width

        if height > screen_height:
            screen_height = height

    mod = sys.modules['__main__']

    setattr(mod, 'WIDTH', screen_width)
    setattr(mod, 'HEIGHT', screen_height)

    # noinspection PyTypeChecker
    screen = None
    scale_surface = None
    if width < screen_width or height < screen_height:
        scale_surface = pygame.Surface((width, height))

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

    global __execute
    __execute = True
    pgzrun.go()


def terminate_on_desktop():
    """
    Terminates the application by ending the execute() function.
    """
    global __execute
    __execute = False
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def terminate_on_microcontroller():
    """
    Terminates the application when running on a microcontroller.
    """
    global __execute
    __execute = False


# Bind the correct execution function based on the system.
if is_running_on_microcontroller():
    execute = execute_on_microcontroller
    terminate = terminate_on_microcontroller

if is_running_on_desktop():
    execute = execute_on_desktop
    terminate = terminate_on_desktop

################################################################################
# C O N F I G    A N D    D E P E N D E N C I E S
################################################################################
config = None


def import_config():
    """
    Loads or reloads the config file. This is called automatically when the module
    is first loaded so only needs to be called if 'config.py' changes and we need
    to see those changes. Ordinarily this is only useful when testing.

    Please note that this is additive so if the config file changes, the new
    values will be added to the existing configuration. Redefined values will
    be overwritten by removed values will not be deleted.
    """
    global config
    try:
        config = importlib.import_module('config')
        config = importlib.reload(config)
        print(f"Config file {config.__file__} loaded.")

        # noinspection PyTypeChecker
        with open(config.__file__) as f:
            print(f.read())


    except ImportError:
        print("No config file found.")


import_config()

if is_running_on_desktop():
    # This is required to bootstrap the pygame display to allow some of the
    # game setup code to work.
    import pgzrun
    import pygame

if is_running_on_microcontroller():
    # This is required on microcontrollers as we implement the game loop
    # ourselves.
    import time

# Initialise the device next to allow it to perform any setup.
import_driver('device')
