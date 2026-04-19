"""
This is the most basic test that bootstraps the application and
runs it for a defined runtime, reporting the average number of
update cycles per second
"""
import tests.validate_device.helper as helper

runtime = 1
update_cycles = 0


def execute():
    import time

    from pmpge.game import Game

    game: Game = Game()

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
    helper.start_validation()
    execute()
    helper.end_validation()
