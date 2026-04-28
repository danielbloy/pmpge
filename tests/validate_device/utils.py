"""
This module contains all the setup and instrumentation code to assist executing
the on device validation and profiling. The only function you should need to use
is execute() as it bootstraps everything else.
"""
import gc
import time

from pmpge.environment import is_running_on_desktop, config
from pmpge.game import Game
from pmpge.sprite import Sprite
from pmpge.traits.physics import Velocity
from pmpge.traits.sprites import SpriteImage

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable

RUNTIME = 1
SAMPLE_FREQUENCY = 10
REPORT_FREQUENCY = 1
PROFILE = False
PROFILE_TOP = 10

if hasattr(config, 'RUNTIME'):
    RUNTIME = config.RUNTIME

if hasattr(config, 'SAMPLE_FREQUENCY'):
    SAMPLE_FREQUENCY = config.SAMPLE_FREQUENCY

if hasattr(config, 'REPORT_FREQUENCY'):
    REPORT_FREQUENCY = config.REPORT_FREQUENCY

if hasattr(config, 'PROFILE'):
    PROFILE = config.PROFILE

if hasattr(config, 'PROFILE_TOP'):
    PROFILE_TOP = config.PROFILE_TOP


class SpriteData:
    x: int
    y: int
    vx: int
    vy: int
    image: str
    sprite: Sprite

    def __init__(self, x: int, y: int, vx: int, vy: int, image: str):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image = image


def create_sprites(game: Game, sprite_data: list[SpriteData]):
    """
    Simple utility method to create a range of sprites at the root of the
    Game instance
    """
    for data in sprite_data:
        sprite = Sprite(
            data.x, data.y,
            Velocity(data.vx, data.vy),
            SpriteImage(data.image))
        data.sprite = sprite
        game.add_child(sprite)


def add_update_method(game: Game, callable: Callable[[Game], None], fps: int = 5):
    """
    Adds an update method to a Game instance that gets called at the desired fps (roughly).
    """
    next_call = None
    call_delta = 1 / fps

    def inner(dt):
        nonlocal next_call
        if next_call is None:
            next_call = time.monotonic()

        now = time.monotonic()

        if now >= next_call:
            next_call += call_delta
            callable(game)

    game.add_update_func(inner)


def should_execute(name: str):
    """
    Used to determine is we are running as a main module or not.
    """
    if name == '__main__':
        return True

    if is_running_on_desktop():
        return name == "pgzero.builtins"

    return False


def execute(
        setup_func: Callable[[Game], None],
        runtime: int = RUNTIME,
        sample_frequency: int = SAMPLE_FREQUENCY,
        report_frequency: int = REPORT_FREQUENCY):
    """
    Instruments and executes the Game, reporting all details out afterwards.
    A single Game instance is created with update() and draw() functions
    attached which count the number of cycles executed as well as terminating
    after the desired number of seconds. The memory usage is also tracked, which
    is expensive so the recording and reporting rate are configurable from defaults.

    @param setup_func - Called to setup the Game instance
    @param runtime - The number of seconds to execute for
    @param sample_frequency - The number of memory samples per second.
    @param report_frequency - The number of time to report memory usage per second.
    """
    sample_period = 1_000_000_000 // sample_frequency
    last_sample = 0

    reporting_period = 1_000_000_000 // report_frequency
    last_report = 0

    def monitor_ram(dt: float):
        """
        Samples and reports the memory usage at the required frequencies.
        """
        nonlocal last_sample, last_report
        now = time.monotonic_ns()

        sample = (now - last_sample) >= sample_period
        report = (now - last_report) >= reporting_period

        if sample:
            last_sample = now
            __sample_memory_usage()

        if report:
            last_report = now
            __report_memory_usage()

    update_cycles = 0

    def update(dt: float):
        nonlocal update_cycles
        update_cycles += 1

        if time.monotonic() > finish:
            game.terminate()

    draw_cycles = 0

    def draw(surface):
        nonlocal draw_cycles
        draw_cycles += 1

    game: Game = Game(160, 120)
    setup_func(game)
    game.add_update_func(monitor_ram)
    game.add_update_func(update)
    game.add_draw_func(draw)

    __reset_memory_usage()
    __start_profiling()
    finish = time.monotonic() + runtime + 0.05  # ake sure we get the start AND finish reports.
    game.run()
    __end_profiling()

    print(f"Achieved {update_cycles / runtime:.2f} updates/s")
    print(f"Achieved {draw_cycles / runtime:.2f} draws/s")

    # Free all memory and reset
    del game
    gc.collect()
    sample_period, last_sample, reporting_period, last_report = 0, 0, 0, 0
    monitor_ram(0)


__peak_used_ram = 0
__used_ram = 0
__free_ram = 0
__total_ram = 0


def __reset_memory_usage():
    global __peak_used_ram, __used_ram, __free_ram, __total_ram
    __peak_used_ram = 0
    __used_ram = 0
    __free_ram = 0
    __total_ram = 0


def __sample_memory_usage():
    global __peak_used_ram, __used_ram, __free_ram, __total_ram

    if is_running_on_desktop():
        import psutil as psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        __used_ram = stats.total / 1_048_576
        __free_ram = stats.free / 1_048_576
        __total_ram = stats.used / 1_048_576
    else:
        __used_ram = gc.mem_alloc()
        __free_ram = gc.mem_free()
        __total_ram = __used_ram + __free_ram

    if __used_ram > __peak_used_ram:
        __peak_used_ram = __used_ram


def __report_memory_usage():
    if is_running_on_desktop():
        print(
            f"Peak: {__peak_used_ram:.2f} MB, Used: {__used_ram:.2f} MB, Free: {__free_ram:.2f} MB, Total: {__total_ram:.2f} MB")
    else:
        print(
            f"Peak: {__peak_used_ram} bytes, Used: {__used_ram} bytes, Free: {__free_ram} bytes, Total: {__total_ram} bytes")


def __start_profiling():
    # See: https://docs.python.org/3/library/tracemalloc.html
    # And: https://stackoverflow.com/questions/552744/how-do-i-profile-memory-usage-in-python
    if is_running_on_desktop() and PROFILE:
        import tracemalloc
        tracemalloc.start()


def __end_profiling(top: int = PROFILE_TOP):
    if is_running_on_desktop() and PROFILE:
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print(f"[ Top {top} ]")
        for stat in top_stats[:top]:
            print(stat)
