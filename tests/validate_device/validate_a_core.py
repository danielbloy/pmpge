"""
This is the most basic test that bootstraps the application and
runs it for a second. Enable the debug to see memory usage
output as the program executes.
"""
import tests.validate_device.helper as helper

DEBUG = False
update_cycles = 0


def execute():
    import time

    from pmpge.game import Game

    game: Game = Game()

    def terminate(dt: float):
        global update_cycles
        update_cycles += 1
        helper.track_memory_usage(DEBUG)

        if time.monotonic() > finish:
            game.terminate()

    game.add_update_func(terminate)

    finish = time.monotonic() + 1
    game.run()
    print(f"Achieved {update_cycles} update cycles")


if helper.should_execute(__name__):
    execute()
    helper.report_memory_usage()
