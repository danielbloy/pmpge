import gc
import time

import pmpge.environment as environment

peak = 0
last_report = 0


def should_execute(name: str):
    if name == '__main__':
        return True

    if environment.is_running_on_desktop():
        return name == "pgzero.builtins"

    return False


# TODO: Improve the documentation on these tests.

def start_validation():
    # See: https://docs.python.org/3/library/tracemalloc.html
    if environment.is_running_on_desktop():
        import tracemalloc
        tracemalloc.start()


def end_validation():
    if environment.is_running_on_desktop():
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print("[ Top 20 ]")
        for stat in top_stats[:20]:
            print(stat)

    report_memory_usage_and_free()


def track_memory_usage(report: bool = False):
    global peak
    if environment.is_running_on_desktop():
        import psutil as psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        total_ram = stats.total / 1_048_576
        free_ram = stats.free / 1_048_576
        used_ram = stats.used / 1_048_576
        if used_ram > peak:
            peak = used_ram
        if report:
            print(f"Peak: {peak:.2f} MB, Used: {used_ram:.2f} MB, Free: {free_ram:.2f} MB, Total: {total_ram:.2f} MB")
    else:
        alloc = gc.mem_alloc()
        if alloc > peak:
            peak = alloc
        if report:
            print(f"Peak: {peak} bytes, Used: {alloc} bytes, Free: {gc.mem_free()} bytes")


def report_memory_usage_periodically(period: int = 1_000_000_100):
    """
    Reports memory usage at the required period (in nanoseconds)
    """
    global last_report
    now = time.monotonic_ns()
    report = (now - last_report) >= period
    track_memory_usage(report)
    if report:
        last_report = now


def report_memory_usage():
    track_memory_usage(True)


def report_memory_usage_and_free():
    global peak
    report_memory_usage()
    gc.collect()
    peak = 0
    report_memory_usage()
