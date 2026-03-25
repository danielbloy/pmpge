class Velocity:
    def __init__(self, vx, vy: int):
        self.vx: int = vx
        self.vy: int = vy

    def update(self, dt: float):
        self.x += dt * self.vx
        self.y += dt * self.vy


class Acceleration:
    def __init__(self, ax, ay: int):
        self.ax: int = ax
        self.ay: int = ay

    def update(self, dt: float):
        self.vx += dt * self.ax
        self.vy += dt * self.ay


class Friction:
    """
    Friction is an opposing force against the motion of a sprite. If a sprite has a velocity, then
    its friction will slow the sprite down until the velocity becomes zero. This is similar to
    a negative acceleration, but friction stops once the sprite stops.
    """

    def __init__(self, fx, fy: int):
        self.fx: int = fx
        self.fy: int = fy

    def update(self, dt: float):
        if self.vx > 0:
            self.vx -= dt * self.fx

        if self.fy > 0:
            self.vy -= dt * self.fy
