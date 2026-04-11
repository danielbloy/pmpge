from pmpge.controller import Controller


class MoveWithController:
    """
    MoveWithController uses a Controller object to move the GameObject either
    horizontally, vertically or both by a specified velocity in pixels per second.

    The Controller must have a left and right button but can optionally have up
    and down buttons. This allows it to be used with 2 button controllers and up.

    The MoveWithController trait requires a Position trait to be present on the
    GameObject.
    """

    x: float
    y: float
    mx: int
    my: int
    controller: Controller

    def __init__(self, mx, my: int, controller: Controller):
        self.mx = mx
        self.my = my
        self.controller = controller

    def update(self, dt: float):
        new_x = self.x
        new_y = self.y
        controller = self.controller

        if controller.left:
            new_x = new_x - (self.mx * dt)
        elif controller.right:
            new_x = new_x + (self.mx * dt)

        if controller.button_count >= 6:
            if controller.up:
                new_y = new_y - (self.my * dt)
            elif controller.down:
                new_y = new_y + (self.my * dt)

        self.x = new_x
        self.y = new_y
