"""
Creates a large number of GameObjects to see memory usage.
"""
import tests.validate_device.helper as helper

runtime = 1
update_cycles = 0


def execute():
    import time

    from pmpge.game import Game
    from pmpge.game_object import GameObject

    game: Game = Game()
    for _ in range(200):
        game.add_child(GameObject())

    def terminate(dt: float):
        global update_cycles
        update_cycles += 1
        helper.report_memory_usage_periodically()

        if time.monotonic() > finish:
            game.terminate()

    game.add_update_func(terminate)

    finish = time.monotonic() + runtime
    game.run()
    print(f"Achieved {update_cycles / runtime:.2f} update cycles per second")


if helper.should_execute(__name__):
    execute()
    helper.report_memory_usage()
