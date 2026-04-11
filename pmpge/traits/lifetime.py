class Lifetime:
    """
    Lifetime provides a way for a GameObject to have a limited lifespan. If set to None, lifetime
    is infinite. Once set to a number, lifetime begins to count down to zero at which point it
    will automatically mark itself for destruction. You can keep a GameObject alive for longer
    by adjusting the value of lifetime.

    Lifetime only works as a Trait of GameObject as it requires a destroy() method.
    """
    lifetime: float | None

    def __init__(self, lifetime: float = None):
        self.lifetime = lifetime

    def update(self, dt: float):
        if self.lifetime:
            self.lifetime -= dt
            if self.lifetime <= 0:
                # noinspection PyUnresolvedReferences
                self.destroy()
