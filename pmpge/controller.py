"""
There are a several primary controller levels, defined by a number. Each HAL
will support up to an including one of the levels. Each level add progressively
more buttons than the previous. Instantiating a Controller instance will give
you a controller representing the greatest level supported. Each controller
format is defined below (all controllers have a menu and start button):

  * 0 - AB button controller
  * 1 - NES style controller
  * 2 - SNES style controller without shoulder buttons
  * 3 - SNES style controller with shoulder buttons

There are also some named actions that are mapped to buttons:

  * Action
  * Cancel

Button arrangements for each controller:

0 - AB

      B            A    (B and A are also mapped as Left and right respectively)
      
    Start       Select  (start is mapped as action, select as cancel)

1 - NES

      U        
    L   R           A    (A is mapped as action, B as cancel)
      D           B

    Start       Select

2 - SNES without shoulder buttons

      U           X
    L   R       Y   A    (A is mapped as action, B as cancel)
      D           B

    Start       Select

3 - SNES with shoulder buttons

 L Shoulder   R Shoulder

      U           X
    L   R       Y   A    (A is mapped as action, B as cancel)
      D           B

    Start       Select
"""
from abc import ABC, abstractmethod

import pmpge.environment as environment


class ABController(ABC):

    @property
    def level(self):
        return 0

    @property
    @abstractmethod
    def start(self) -> bool:
        pass

    @property
    @abstractmethod
    def select(self) -> bool:
        pass

    @property
    def action(self) -> bool:
        return self.start

    @property
    def cancel(self) -> bool:
        return self.select

    @property
    @abstractmethod
    def a(self) -> bool:
        pass

    @property
    @abstractmethod
    def b(self) -> bool:
        pass

    @property
    def left(self) -> bool:
        return self.b

    @property
    def l(self) -> bool:
        return self.b

    @property
    def right(self) -> bool:
        return self.a

    @property
    def r(self) -> bool:
        return self.a


class NESController(ABC):

    @property
    def level(self):
        return 1

    @property
    @abstractmethod
    def start(self) -> bool:
        pass

    @property
    @abstractmethod
    def select(self) -> bool:
        pass

    @property
    def action(self) -> bool:
        return self.a

    @property
    def cancel(self) -> bool:
        return self.b

    @property
    @abstractmethod
    def left(self) -> bool:
        pass

    @property
    def l(self) -> bool:
        return self.left

    @property
    @abstractmethod
    def right(self) -> bool:
        pass

    @property
    def r(self) -> bool:
        return self.right

    @property
    @abstractmethod
    def up(self) -> bool:
        pass

    @property
    def u(self) -> bool:
        return self.up

    @property
    @abstractmethod
    def down(self) -> bool:
        pass

    @property
    def d(self) -> bool:
        return self.down

    @property
    @abstractmethod
    def a(self) -> bool:
        pass

    @property
    @abstractmethod
    def b(self) -> bool:
        pass


class SNESNoShoulderButtonsController(ABC):

    @property
    def level(self):
        return 2

    @property
    @abstractmethod
    def start(self) -> bool:
        pass

    @property
    @abstractmethod
    def select(self) -> bool:
        pass

    @property
    def action(self) -> bool:
        return self.a

    @property
    def cancel(self) -> bool:
        return self.b

    @property
    @abstractmethod
    def left(self) -> bool:
        pass

    @property
    def l(self) -> bool:
        return self.left

    @property
    @abstractmethod
    def right(self) -> bool:
        pass

    @property
    def r(self) -> bool:
        return self.right

    @property
    @abstractmethod
    def up(self) -> bool:
        pass

    @property
    def u(self) -> bool:
        return self.up

    @property
    @abstractmethod
    def down(self) -> bool:
        pass

    @property
    def d(self) -> bool:
        return self.down

    @property
    @abstractmethod
    def a(self) -> bool:
        pass

    @property
    @abstractmethod
    def b(self) -> bool:
        pass

    @property
    @abstractmethod
    def x(self) -> bool:
        pass

    @property
    @abstractmethod
    def y(self) -> bool:
        pass


class SNESController(ABC):

    @property
    def level(self):
        return 3

    @property
    @abstractmethod
    def start(self) -> bool:
        pass

    @property
    @abstractmethod
    def select(self) -> bool:
        pass

    @property
    def action(self) -> bool:
        return self.a

    @property
    def cancel(self) -> bool:
        return self.b

    @property
    @abstractmethod
    def left(self) -> bool:
        pass

    @property
    def l(self) -> bool:
        return self.left

    @property
    @abstractmethod
    def right(self) -> bool:
        pass

    @property
    def r(self) -> bool:
        return self.right

    @property
    @abstractmethod
    def up(self) -> bool:
        pass

    @property
    def u(self) -> bool:
        return self.up

    @property
    @abstractmethod
    def down(self) -> bool:
        pass

    @property
    def d(self) -> bool:
        return self.down

    @property
    @abstractmethod
    def a(self) -> bool:
        pass

    @property
    @abstractmethod
    def b(self) -> bool:
        pass

    @property
    @abstractmethod
    def x(self) -> bool:
        pass

    @property
    @abstractmethod
    def y(self) -> bool:
        pass

    @property
    @abstractmethod
    def left_shoulder(self) -> bool:
        pass

    @property
    def ls(self) -> bool:
        return self.left

    @property
    @abstractmethod
    def right_shoulder(self) -> bool:
        pass

    @property
    def rs(self) -> bool:
        return self.right


__controller = environment.import_hal_module('controller')
Controller = __controller.Controller
