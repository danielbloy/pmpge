import math

import pytest

from pmpge.environment import RateLimiter


def test_rate_must_be_positive():
    """
    Simple validation tests
    """
    with pytest.raises(ValueError):
        RateLimiter(lambda _: None, rate=0)

    with pytest.raises(ValueError):
        RateLimiter(lambda _: None, rate=-1)


def test_always_fires_on_first_update():
    """
    The first time a RateLimiter is called, it should call the callback
    function, regardless of how much time has passed.
    """
    elapsed_time: float = 0.0
    callback_count: int = 0

    def callback(dt: float):
        nonlocal elapsed_time, callback_count
        elapsed_time = dt
        callback_count += 1

    rl = RateLimiter(callback, rate=1)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 0
    rl(0)
    rl(0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 1

    rl = RateLimiter(callback, rate=100)
    rl(0)
    rl(0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 2

    rl = RateLimiter(callback, rate=1)
    rl(0.1)
    rl(0)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 3


def test_fires_at_correct_rate():
    """
    Validates that the callback is called at the rate required.
    This also validates that the interval is correct.
    """
    elapsed_time_1: float = 0.0
    callback_count_1: int = 0

    def callback_1(dt: float):
        nonlocal elapsed_time_1, callback_count_1
        elapsed_time_1 = dt
        callback_count_1 += 1

    elapsed_time_2: float = 0.0
    callback_count_2: int = 0

    def callback_2(dt: float):
        nonlocal elapsed_time_2, callback_count_2
        elapsed_time_2 = dt
        callback_count_2 += 1

    elapsed_time_5: float = 0.0
    callback_count_5: int = 0

    def callback_5(dt: float):
        nonlocal elapsed_time_5, callback_count_5
        elapsed_time_5 = dt
        callback_count_5 += 1

    rl_1 = RateLimiter(callback_1, rate=1)  # 1 second per invocation
    rl_2 = RateLimiter(callback_2, rate=2)  # 0.5 seconds per invocation
    rl_5 = RateLimiter(callback_5, rate=5)  # 0.2 seconds per invocation

    # All should fire on the first invocation
    rl_1(0.0)
    rl_2(0.0)
    rl_5(0.0)
    assert math.isclose(elapsed_time_1, 0.0)
    assert callback_count_1 == 1
    assert math.isclose(elapsed_time_2, 0.0)
    assert callback_count_2 == 1
    assert math.isclose(elapsed_time_5, 0.0)
    assert callback_count_5 == 1

    # 0.1 seconds pass and nothing should fire (0.1 seconds elapsed)
    rl_1(0.1)
    rl_2(0.1)
    rl_5(0.1)
    assert math.isclose(elapsed_time_1, 0.0)
    assert callback_count_1 == 1
    assert math.isclose(elapsed_time_2, 0.0)
    assert callback_count_2 == 1
    assert math.isclose(elapsed_time_5, 0.0)
    assert callback_count_5 == 1

    # A further 0.1 seconds should fire rl_5 (0.2 seconds elapsed)
    rl_1(0.1)
    rl_2(0.1)
    rl_5(0.1)
    assert math.isclose(elapsed_time_1, 0.0)
    assert callback_count_1 == 1
    assert math.isclose(elapsed_time_2, 0.0)
    assert callback_count_2 == 1
    assert math.isclose(elapsed_time_5, 0.2)
    assert callback_count_5 == 2

    # A further 0.1 seconds should fire nothing (0.3 seconds elapsed)
    rl_1(0.1)
    rl_2(0.1)
    rl_5(0.1)
    assert math.isclose(elapsed_time_1, 0.0)
    assert callback_count_1 == 1
    assert math.isclose(elapsed_time_2, 0.0)
    assert callback_count_2 == 1
    assert math.isclose(elapsed_time_5, 0.2)
    assert callback_count_5 == 2

    # A further 0.3 seconds should fire both rl_2 and rl_5 (0.6 seconds elapsed)
    # Notice that rl_5 will have skipped a call so it's elapsed time is double
    # if it had a perfect rate.
    rl_1(0.3)
    rl_2(0.3)
    rl_5(0.3)
    assert math.isclose(elapsed_time_1, 0.0)
    assert callback_count_1 == 1
    assert math.isclose(elapsed_time_2, 0.6)
    assert callback_count_2 == 2
    assert math.isclose(elapsed_time_5, 0.4)
    assert callback_count_5 == 3

# TODO: More finese in timinng
# TODO: Test rate limit does not fire until counter passed.
# TODO: Test rate limit catches up.
