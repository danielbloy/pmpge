"""
Creates a large number of GameObjects to see memory usage.
"""
import tests.validate_device.helper as helper

DEBUG = False


def execute():
    import time

    from pmpge.game import Game
    from pmpge.game_object import GameObject

    game: Game = Game()
    for _ in range(200):
        game.add_child(GameObject())

    def terminate(dt: float):
        helper.track_memory_usage(DEBUG)

        if time.monotonic() > finish:
            game.terminate()

    game.add_update_func(terminate)

    finish = time.monotonic() + 1
    game.run()


if helper.should_execute(__name__):
    execute()
    helper.report_memory_usage()
