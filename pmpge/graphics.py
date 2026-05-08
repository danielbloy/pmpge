import pmpge.environment as environment

# These are not available in CircuitPython.
if environment.is_running_on_desktop():
    from typing import Callable

__graphics = environment.import_driver('graphics')
DriverImageResource = __graphics.DriverImageResource
GraphicsDrawImageTrait = __graphics.GraphicsDrawImageTrait
game_object_hierarchy_changed = __graphics.game_object_hierarchy_changed


# TODO: Note these cannot be shared. The underlying bitmap may be shared but this could have
#       image state
class ImageResource(DriverImageResource):
    """
    Represents an image resource that can be loaded and drawn. The actual image
    loading and drawing is done by the graphics driver. Setting the name property
    will trigger a reload of the image. There is an optional notify callback that
    is called with the new width and height of the image after a successful reload.

    # TODO: Document the requirements of DriverImageResource
    """
    width: int
    height: int
    offset_x: int  # TODO: Document what this is for.
    offset_y: int
    _name: str
    notify: Callable[[], None] | None

    def __init__(self, name: str, centered: bool = True, notify: Callable[[], None] = None):
        self.centered = centered
        self.width = 0
        self.height = 0
        self.offset_x = 0
        self.offset_y = 0
        self.notify = notify
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.width, self.height = self.load(value)
        if self.centered:
            self.offset_x = self.width // 2
            self.offset_y = self.height // 2
        else:
            self.offset_x = 0
            self.offset_y = 0

        if self.notify:
            self.notify()

        # TODO: Note that render is implementation specific
