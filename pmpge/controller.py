"""
The controller configuration is based on 12 button SNES controller as follows:

      U           X
    L   R       Y   A
      D           B

    Start       Select

Because the range of devices varies, so does the number of buttons available so all
devices may not support the 12 set of 12 buttons. Common other configurations include:

10 button SNES controller without shoulder buttons:

      U           X
    L   R       Y   A
      D           B

    Start       Select

8 button NES:

      U
    L   R           A
      D           B

    Start       Select

There are lots of other configurations possible too depending on the device.
"""

import pmpge.environment as environment

__controller = environment.import_driver('controller')
ControllerButtons = __controller.ControllerButtons


# Support the following events:
#   button_pressed
#   button_released
# FUTURE: Repeat

# TODO: Need a way to get information about the buttons supported by the device.

class Controller(ControllerButtons):

    @property
    def left(self) -> bool:
        return self.l

    @property
    def right(self) -> bool:
        return self.r

    @property
    def up(self) -> bool:
        return self.u

    @property
    def down(self) -> bool:
        return self.d

    @property
    def left_shoulder(self) -> bool:
        return self.ls

    @property
    def right_shoulder(self) -> bool:
        return self.rs
