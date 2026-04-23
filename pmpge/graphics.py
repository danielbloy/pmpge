from typing import Callable

import pmpge.environment as environment

__graphics = environment.import_driver('graphics')
ImageLoader = __graphics.ImageLoader


class ImageResource(ImageLoader):
    """
    Represents an image resource that can be loaded and drawn. The actual image
    loading and drawing is done by the graphics driver. Setting the name property
    will trigger a reload of the image. There is an optional notify callback that
    is called with the new width and height of the image after a successful reload.
    """
    width: int
    height: int
    _name: str
    notify: Callable[[int, int], None] | None

    def __init__(self, name: str, notify: Callable[[int, int], None] = None):
        self.width = 0
        self.height = 0
        self.notify = notify
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value
        self.load(value)
        notify = self.notify
        if notify:
            notify(self.width, self.height)
