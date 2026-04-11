class Velocity:
    """
    Velocity is the rate at which a sprite moves either horizontally, vertically or
    both. It is measured in pixels per second. If a screen is 160 pixels wide and
    a sprite has a velocity of 40 pixels per second then it will take 4 seconds
    to move across the screen.

    The Velocity trait requires a Position trait to be present on the GameObject.
    """

    x: float
    y: float
    vx: int
    vy: int

    def __init__(self, vx, vy: int):
        self.vx: int = vx
        self.vy: int = vy

    def update(self, dt: float):
        self.x += (dt * self.vx)
        self.y += (dt * self.vy)


class Acceleration:
    """
    Acceleration is the rate at which a sprite changes its velocity. It is measured in pixels
    per second per second. If a stationary sprite has an acceleration of 40 pixels per second
    per second, then after 1 second it will have a velocity of 40 pixels per second. After 2
    seconds it will have a velocity of 80 pixels per second and so on.

    The Acceleration trait requires a Velocity trait to be present on the GameObject.
    """

    vx: int
    vy: int
    ax: int
    ay: int

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

    The Friction trait requires a Velocity trait to be present on the GameObject.
    """

    vx: int
    vy: int
    fx: int
    fy: int

    def __init__(self, fx, fy: int):
        self.fx: int = fx
        self.fy: int = fy

    def update(self, dt: float):
        if self.vx > 0:
            self.vx -= dt * self.fx

        if self.fy > 0:
            self.vy -= dt * self.fy
