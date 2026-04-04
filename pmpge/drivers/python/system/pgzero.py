import sys

import pgzrun

mod = sys.modules['__main__']


def run(width: int = None, height: int = None):
    """
    Desired width and height.
    """
    # TODO: Pull out configuration for actual screen dimensions from configuration
    # If not specified then default to 640x480

    # TODO: Scale from desired to actual
    width = width if width else 640
    height = height if height else 480
    setattr(mod, 'WIDTH', width)
    setattr(mod, 'HEIGHT', height)
    pgzrun.go()
