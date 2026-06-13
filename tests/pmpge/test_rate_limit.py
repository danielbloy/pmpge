from pmpge.environment import RateLimit


def test_rate_limiter_always_fires_on_first_update():
    """
    The first time a RateLimit
    """
    rl = RateLimit()

# TODO: Test rate limit fires on first call.
# TODO: Test rate limit does not fire until counter passed.
# TODO: Test rate limit catches up.
