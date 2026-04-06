class Lifetime:
    # TODO: Document this class
    # TODO: Test this class

    def __init__(self, lifetime: float = None):
        self.lifetime = lifetime

    def update(self, dt: float):
        if self.lifetime:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.destroy = True
                return
