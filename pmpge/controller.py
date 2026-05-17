"""
TODO: Review this documentation
TODO: Consider adding in documentation for the 3 button controller

There are several controller configurations, defined by the number of buttons available
on the device. Each controller builds on the previous controllers as the number of
buttons steadily increases. Instantiating a Controller instance will give you a
controller representing the greatest number of buttons supported on the device.
Each controller format is defined below (all controllers have a menu and start button):

  * 0  - No buttons
  * 2  - 2 button controller                               (start and select)
  * 3  - 3 button controller                               (start, select, A)
  * 4  - AB controller                                     (start, select, A, B)
  * 6 -  AB UD controller                                  (start, select, U, D, A, B)
  * 8  - NES style controller                              (start, select, U, D, L, R, A, B)
  * 10 - SNES style controller without shoulder buttons    (start, select, U, D, L, R, A, B, X, Y)
  * 12 - SNES style controller with shoulder buttons       (start, select, U, D, L, R, A, B, X, Y, LS, RS)

There are also some named actions that are mapped to buttons:

  * Action
  * Cancel

Button arrangements for each controller:

2 - 2 button controller

    Start       Select  (start is mapped as action, select as cancel)

4 - AB

      B            A    (B and A are also mapped as Left and right respectively)
      
    Start       Select  (start is mapped as action, select as cancel)


6 - AB UD

            U
      B            A    (B and A are also mapped as Left and right respectively)
            D

    Start       Select  (start is mapped as action, select as cancel)

8 - NES

      U        
    L   R           A    (A is mapped as action, B as cancel)
      D           B

    Start       Select

10 - SNES without shoulder buttons

      U           X
    L   R       Y   A    (A is mapped as action, B as cancel)
      D           B

    Start       Select

12 - SNES with shoulder buttons

 L Shoulder   R Shoulder

      U           X
    L   R       Y   A    (A is mapped as action, B as cancel)
      D           B

    Start       Select
"""

import pmpge.environment as environment


class Controller:

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
    def action(self) -> bool:
        return self.a

    @property
    def cancel(self) -> bool:
        return self.b

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


__controller = environment.import_driver('controller')
