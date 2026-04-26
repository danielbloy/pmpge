# This file sets up some variables that are determined from the environment
# that the code is being executed in to allow various parts of the program
# to selectively run based on what is available to it.
#
# THIS FILE SHOULD NOT IMPORT ANY OTHER FILE IN THE FRAMEWORK OTHER THAN DRIVERS
#
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

    if hasattr(config, 'SCREEN_WIDTH'):
        width = config.SCREEN_WIDTH

    if hasattr(config, 'SCREEN_HEIGHT'):
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
    if hasattr(config, 'CONTROLLER_DRIVER'):
        return config.CONTROLLER_DRIVER

    if is_running_on_desktop():
        return "pmpge.drivers.controller.pgzero"

    return "pmpge.drivers.controller.none"


def get_device_driver() -> str:
    """
    Returns the device driver to use. This can be specified in `config.py` to provide
    an override, otherwise the `none.py` device driver will be used. This is different
    from the other drivers which have system specific drivers.
    """
    if hasattr(config, 'DEVICE_DRIVER'):
        return config.DEVICE_DRIVER

    return "pmpge.drivers.device.none"


def get_graphics_driver() -> str:
    """
    Returns the graphics driver to use. This can be specified in `config.py` to provide
    an override, otherwise a default will be provided depending on the system we are
    executing within.
    """
    if hasattr(config, 'GRAPHICS_DRIVER'):
        return config.GRAPHICS_DRIVER

    if is_running_on_desktop():
        return "pmpge.drivers.graphics.pgzero"

    return "pmpge.drivers.graphics.none"


def get_sound_driver() -> str:
    """
    Returns the sound driver to use. This can be specified in `config.py` to provide
    an override, otherwise a default will be provided depending on the system we are
    executing within.
    """
    if hasattr(config, 'SOUND_DRIVER'):
        return config.SOUND_DRIVER

    if is_running_on_desktop():
        return "pmpge.drivers.sound.pgzero"

    return "pmpge.drivers.sound.none"


def get_driver(module: str) -> str:
    """
    Returns the specified driver for the given module. Valid modules are:
      * controller
      * device
      * graphics
      * sound
    """
    if module.lower() == "controller":
        return get_controller_driver()

    if module.lower() == "device":
        return get_device_driver()

    if module.lower() == "graphics":
        return get_graphics_driver()

    if module.lower() == "sound":
        return get_sound_driver()

    raise ValueError("Unknown module")


def import_driver(module: str):
    """
    Returns the specified driver for the given module. This is trivial on a
    full CPython implementation as we can use the official importlib module.
    However, on a MicroController, this is not available so we have to load
    it ourselves. See the following articles for more information about what
    we are attempting to do here:
    * https://github.com/adafruit/circuitpython/issues/10481 - contains a link
      to a pure Python importlib.reload() function.
    * https://github.com/Lumensalis/LumensalisCPLib/blob/main/lib/LumensalisCP/pyCp/importlib.py
      The importlib.reload() function.
    * https://stackoverflow.com/questions/9806963/how-to-use-the-import-function-to-import-a-name-from-a-submodule
      Article on how to use __import__().
    """
    driver = get_driver(module)

    if is_running_on_desktop():
        import importlib.util
        return importlib.import_module(driver)
    else:
        # TODO: We may need a MicroPython specific version of this code.
        # TODO: This could benefit from further investigation to see if we can
        #       do something better.
        mod = __import__(driver)
        mod = sys.modules[driver]
        return mod


################################################################################
# E X E C U T I O N
################################################################################

__execute: bool = False


def terminate():
    """
    Terminates the application by ending the execute() function.
    """
    global __execute
    __execute = False
    if is_running_on_desktop():
        pygame.event.post(pygame.event.Event(pygame.QUIT))


def execute(game, background_colour: tuple[int, int, int] = None):
    """
    Executes the game at the desired resolution. If the screen display is larger than
    the specified width and height, the application will scale if it is able to do so.

    In a desktop environment, this function also injects draw() and update() functions
    into the main application to hook into pygame zero. This will overwrite those
    functions if they are set in the main Python file.
    """
    if not background_colour:
        background_colour = (0, 0, 0)

    width, height = game.width, game.height
    screen_width, screen_height = screen_size()

    # On a microcontroller, a larger game size than screen size is an error.
    if is_running_on_microcontroller():
        if width > screen_width or height > screen_height:
            raise ValueError("Game width and height cannot be larger than screen")

    device = import_driver('device')
    controller = import_driver('controller')
    sound = import_driver('sound')
    graphics = import_driver('graphics')

    device.init() if hasattr(device, 'init') else None
    controller.init() if hasattr(controller, 'init') else None
    sound.init() if hasattr(sound, 'init') else None
    graphics.init(width, height, screen_width, screen_height, background_colour) if hasattr(graphics, 'init') else None

    device_update = device.update if hasattr(device, 'update') else None
    controller_update = controller.update if hasattr(controller, 'update') else None
    sound_update = sound.update if hasattr(sound, 'update') else None
    graphics_update = graphics.update if hasattr(graphics, 'update') else None

    try:
        def update(dt: float):
            device_update(dt) if device_update else None
            controller_update(dt) if controller_update else None
            sound_update(dt) if sound_update else None
            graphics_update(dt) if graphics_update else None
            game.update(dt)

        def draw(surface):
            graphics.clear(surface)
            game.draw(surface)
            graphics.draw(surface)

        global __execute
        __execute = True

        if is_running_on_desktop():
            # On a desktop environment, we need to inject our own draw() and update()
            # methods to interact with pygame zero.
            mod = sys.modules['__main__']
            screen = None

            def pgzero_draw():
                nonlocal screen
                if not screen:
                    screen = getattr(mod, 'screen')

                draw(screen)

            setattr(mod, 'draw', pgzero_draw)
            setattr(mod, 'update', update)

            pgzrun.go()

        else:
            # On a microcontroller, we implement our own game loop.
            last = time.monotonic()
            while __execute:
                now = time.monotonic()
                delta_time = now - last
                last = now

                update(delta_time)
                draw(None)

    finally:
        __execute = False

        graphics.deinit() if hasattr(graphics, 'deinit') else None
        sound.deinit() if hasattr(sound, 'deinit') else None
        controller.deinit() if hasattr(controller, 'deinit') else None
        device.deinit() if hasattr(device, 'deinit') else None


################################################################################
# C O N F I G    A N D    D E P E N D E N C I E S
################################################################################
config = None


def import_config():
    """
    Loads or reloads the config file. This is called automatically when the module
    is first loaded, so it only needs to be called if 'config.py' changes and we need
    to see those changes. Ordinarily this is only useful when testing.

    Please note that this is additive, so if the config file changes, the new
    values will be added to the existing configuration. Redefined values will
    be overwritten by removed values will not be deleted.
    """
    global config
    try:
        if is_running_on_desktop():
            # noinspection PyUnusedImports
            import importlib.util
            config = importlib.import_module('config')
            config = importlib.reload(config)
        else:
            # TODO: This could benefit from further investigation to see if we can
            #       do something better. See the notes in import_driver().
            config = __import__('config')

        print(f"Config file {config.__file__} loaded.")

        # noinspection PyTypeChecker
        with open(config.__file__) as f:
            print(f.read())


    except ImportError:
        print("No config file found.")

    # If there was not a config file found then we create a placeholder instance.
    if not config:
        config = type('Config', (), {})()


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

# Now we will do some device specific initialisation providing defaults
if is_running_on_circuitpython():
    try:
        # noinspection PyUnusedImports,PyPackageRequirements
        import board as board

        # If the board has a built-in display, we provide the screen width,
        # screen height and graphics driver if they have not been provided.
        if hasattr(board, 'DISPLAY'):
            display = board.DISPLAY
            print("Device has built-in display")
            if not hasattr(config, 'SCREEN_WIDTH'):
                config.SCREEN_WIDTH = display.width
                print(f"Setting SCREEN_WIDTH = {config.SCREEN_WIDTH}")

            if not hasattr(config, 'SCREEN_HEIGHT'):
                config.SCREEN_HEIGHT = display.height
                print(f"Setting SCREEN_HEIGHT = {config.SCREEN_HEIGHT}")

            if not hasattr(config, 'GRAPHICS_DRIVER'):
                config.GRAPHICS_DRIVER = "pmpge.drivers.graphics.displayio"
                print(f"Setting GRAPHICS_DRIVER = {config.GRAPHICS_DRIVER}")

    except ImportError:
        pass

# Initialise the device next to allow it to perform any setup.
import_driver('device')
