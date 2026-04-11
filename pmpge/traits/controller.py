from pmpge.controller import Controller


class MoveWithController:
    """
    MoveWithController uses a Controller object to move the GameObject either
    horizontally, vertically or both by a specified velocity in pixels per second.

    The Controller must have a left and right button but can optionally have up
    and down buttons. This allows it to be used with 2 button controllers and up.

    Because this trait adds a vx and vy property to the GameObject, there is no
    need to combine it with a Velocity trait.

    The MoveWithController trait requires a Position trait to be present on the
    GameObject.
    """

    x: float
    y: float
    vx: int
    vy: int
    controller: Controller

    def __init__(self, vx, vy: int, controller: Controller):
        self.vx = vx
        self.vy = vy
        self.controller = controller

    def update(self, dt: float):
        new_x = self.x
        new_y = self.y
        controller = self.controller

        if controller.left:
            new_x = new_x - (self.vx * dt)
        elif controller.right:
            new_x = new_x + (self.vx * dt)

        if controller.button_count >= 6:
            if controller.up:
                new_y = new_y - (self.vy * dt)
            elif controller.down:
                new_y = new_y + (self.vy * dt)

        self.x = new_x
        self.y = new_y
