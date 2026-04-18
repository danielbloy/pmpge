"""
This is the most basic test that bootstraps the application and
runs it for a second. Enable the debug to see memory usage
output as the program executes.
"""
from tests.validate_device.memory import report_memory_usage, track_memory_usage

DEBUG = False


def execute():
    import time

    from pmpge.game import Game

    game: Game = Game()

    def terminate(dt: float):
        track_memory_usage(DEBUG)

        if time.monotonic() > finish:
            game.terminate()

    game.add_update_func(terminate)

    finish = time.monotonic() + 1
    game.run()


if __name__ == '__main__':
    execute()
    report_memory_usage()
