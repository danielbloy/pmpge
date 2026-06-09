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


class BoundVelocity:
    """
    Limits velocity to a range for each of horizontal and vertical velocities.
    Must be combined with a Velocity trait.
    """
    vx: int
    vy: int
    min_vx: int | None
    max_vx: int | None
    min_vy: int | None
    max_vy: int | None

    def __init__(self,
                 min_vx: int | None = None, max_vx: int | None = None,
                 min_vy: int | None = None, max_vy: int | None = None):

        if min_vx is not None and max_vx is not None:
            if min_vx > max_vx:
                raise ValueError("min_vx cannot be larger than max_vx")

        if min_vy is not None and max_vy is not None:
            if min_vy > max_vy:
                raise ValueError("min_vy cannot be larger than max_vy")

        self.min_vx = min_vx
        self.max_vx = max_vx
        self.min_vy = min_vy
        self.max_vy = max_vy

    def update(self, dt: float):
        max_vx = self.max_vx
        max_vy = self.max_vy
        min_vx = self.min_vx
        min_vy = self.min_vy

        if max_vx is not None:
            self.vx = min(self.vx, max_vx)

        if max_vy is not None:
            self.vy = min(self.vy, max_vy)

        if min_vx is not None:
            self.vx = max(self.vx, min_vx)

        if min_vy is not None:
            self.vy = max(self.vy, min_vy)


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

        if self.vy > 0:
            self.vy -= dt * self.fy


class HorizontalBounce:
    """
    Simple trait that bounces vertically between two points.
    This trait simply flips velocity when it hits the relevant limit
    which changes direction immediately.
    """
    x: float
    vx: int
    x_min: int
    x_max: int

    def __init__(self, x_min, x_max: int):
        self.x_min: int = x_min
        self.x_max: int = x_max

    def update(self, dt: float):
        x = self.x
        vx = self.vx

        if x < self.x_min and vx < 0:
            self.vx = -vx

        if x > self.x_max and vx > 0:
            self.vx = -vx


class VerticalBounce:
    """
    Simple trait that bounces horizontally between two points.
    This trait simply flips velocity when it hits the relevant limit
    which changes direction immediately.
    """
    y: float
    vy: int
    y_min: int
    y_max: int

    def __init__(self, y_min, y_max: int):
        self.y_min: int = y_min
        self.y_max: int = y_max

    def update(self, dt: float):
        y = self.y
        vy = self.vy

        if y < self.y_min and vy < 0:
            self.vy = -vy

        if y > self.y_max and vy > 0:
            self.vy = -vy
