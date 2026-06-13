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


def test_correctly_fires_first_and_second_events():
    """
    Validates that RateLimiter correctly fires the first and second events.
    The first event always fires but the second only when the timer expires.
    """
    elapsed_time: float = 0.0
    callback_count: int = 0

    def callback(dt: float):
        nonlocal elapsed_time, callback_count
        elapsed_time = dt
        callback_count += 1

    rl = RateLimiter(callback, rate=5)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 0

    # First call is at 0.1 seconds which will cause the first event to fire but
    # has not triggered the second event. The elapsed time should equal the initial
    # passed in value. We repeat this test multiple times with multiple values.
    rl(0.0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 1

    rl = RateLimiter(callback, rate=5)
    rl(0.01)
    assert math.isclose(elapsed_time, 0.01)
    assert callback_count == 2

    rl = RateLimiter(callback, rate=5)
    rl(0.1)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 3

    rl = RateLimiter(callback, rate=5)
    rl(0.15)
    assert math.isclose(elapsed_time, 0.15)
    assert callback_count == 4

    # Now we go over to the second trigger. This is also repeated with different values
    callback_count = 0
    rl = RateLimiter(callback, rate=5)
    rl(0.0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 1

    rl(0.2)
    assert math.isclose(elapsed_time, 0.2)
    assert callback_count == 2

    callback_count = 0
    rl = RateLimiter(callback, rate=5)
    rl(0.1)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 1

    rl(0.1)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 2

    callback_count = 0
    rl = RateLimiter(callback, rate=5)
    rl(0.15)
    assert math.isclose(elapsed_time, 0.15)
    assert callback_count == 1

    rl(0.1)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 2

    # Now we test when the initial delay is so long it goes over the second event (the
    # first event is the initial one that is always called). We do this using 2 scenarios
    callback_count = 0
    rl = RateLimiter(callback, rate=5)
    rl(0.3)
    assert math.isclose(elapsed_time, 0.3)
    assert callback_count == 1

    # At this point, the first event was 0.1 seconds over the second event so the second
    # event will get fired, regardless of the time.
    rl(0.0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 2

    # Scenario 2
    callback_count = 0
    rl = RateLimiter(callback, rate=5)
    rl(0.3)
    assert math.isclose(elapsed_time, 0.3)
    assert callback_count == 1

    rl(0.1)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 2


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


def test_correctly_rate_limits():
    """
    Validates that RateLimiter correctly limits the call rate.
    """
    elapsed_time: float = 0.0
    callback_count: int = 0

    def callback(dt: float):
        nonlocal elapsed_time, callback_count
        elapsed_time = dt
        callback_count += 1

    rl = RateLimiter(callback, rate=5)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 0

    # First call is at 0.1 seconds which will cause the first event to fire
    rl(0.1)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 1

    # None of these will trigger the second event, which will not occur until 0.2 seconds
    # have passed.
    rl(0.0)
    rl(0.02)
    rl(0.05)
    assert math.isclose(elapsed_time, 0.1)
    assert callback_count == 1

    # Now we trip the second event.
    rl(0.04)
    assert math.isclose(elapsed_time, 0.11)
    assert callback_count == 2

    # Now we trip the third event which should be 0.19 seconds later.
    rl(0.08)
    rl(0.05)
    rl(0.06)
    assert math.isclose(elapsed_time, 0.19)
    assert callback_count == 3


def test_when_cant_keep_up():
    """
    Validates the RateLimiter when the gaps are so large the desired
    rate cannot be achieved.
    """
    elapsed_time: float = 0.0
    callback_count: int = 0

    def callback(dt: float):
        nonlocal elapsed_time, callback_count
        elapsed_time = dt
        callback_count += 1

    rl = RateLimiter(callback, rate=5)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 0

    # Each call will be so far apart that each invocation will result in a trigger
    rl(0.3)
    assert math.isclose(elapsed_time, 0.3)
    assert callback_count == 1

    rl(0.4)
    assert math.isclose(elapsed_time, 0.4)
    assert callback_count == 2

    rl(0.5)
    assert math.isclose(elapsed_time, 0.5)
    assert callback_count == 3

    rl(0.3)
    assert math.isclose(elapsed_time, 0.3)
    assert callback_count == 4

    # Catches up
    rl(0.0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 5

    # But does not keep triggering
    rl(0.0)
    rl(0.1)
    rl(0.0)
    assert math.isclose(elapsed_time, 0.0)
    assert callback_count == 5
