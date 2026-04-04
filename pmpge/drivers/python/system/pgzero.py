import sys

import pgzrun

mod = sys.modules['__main__']


def initialise(width: int | None = None, height: int | None = None):
    # TODO: Pull out configuration for actual screen dimensions from configuration
    # If not specified then default to 640x480

    # TODO: Scale from desired to actual
    width = width if width else 640
    height = height if height else 480
    setattr(mod, 'WIDTH', width)
    setattr(mod, 'HEIGHT', height)


def execute(game, background_colour: tuple[int, int, int] = None):
    def draw():
        # TODO: See if this can be made better/faster
        screen = getattr(mod, 'screen')
        screen.fill(background_colour)

        game.draw(screen)

    def update(dt):
        game.update(dt)

    setattr(mod, 'draw', draw)
    setattr(mod, 'update', update)

    pgzrun.go()


def terminate():
    sys.exit(0)
