# See https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/basic-debouncing


class XXXXController:

    @property
    def button_count(self):
        return 12

    @property
    def start(self) -> bool:
        pass

    @property
    def select(self) -> bool:
        pass

    @property
    def left(self) -> bool:
        pass

    @property
    def l(self) -> bool:
        return self.left

    @property
    def right(self) -> bool:
        pass

    @property
    def r(self) -> bool:
        return self.right

    @property
    def up(self) -> bool:
        pass

    @property
    def u(self) -> bool:
        return self.up

    @property
    def down(self) -> bool:
        pass

    @property
    def d(self) -> bool:
        return self.down

    @property
    def a(self) -> bool:
        pass

    @property
    def b(self) -> bool:
        pass

    @property
    def x(self) -> bool:
        pass

    @property
    def y(self) -> bool:
        pass

    @property
    def left_shoulder(self) -> bool:
        pass

    @property
    def ls(self) -> bool:
        return self.left

    @property
    def right_shoulder(self) -> bool:
        pass

    @property
    def rs(self) -> bool:
        return self.right


def update():
    # TODO: Cycle through all buttons and update them.
    pass
