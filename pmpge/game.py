from collections.abc import Callable
from typing import Any

from pmpge.environment import screen_size, execute, terminate
from pmpge.game_object import GameObject


class Game:
    """
    Game is the root of the GameObject hierarchy. It provides a simple way to manage the root
    GameObject as well as provide custom draw and update functions that are called after the
    root GameObject is drawn or updated.

    The desired width and height of the game can be specified. If they are not specified then
    the system defaults will be used.
    """

    def __init__(self, width: int = None, height: int = None,
                 background_color: tuple[int, int, int] = None):

        self.background_color: tuple[int, int, int] = background_color if (
            background_color) else (0, 0, 0)

        self.__draw_funcs: list[Callable[[Any], None]] = []
        self.__update_funcs: list[Callable[[float], None]] = []
        self.__root = GameObject(name="root")

        if (width and not height) or (height and not width):
            raise ValueError(
                "Cannot specify just one of width or height, specify both or neither")

        if width and height:
            self.__width, self.__height = width, height
        else:
            self.__width, self.__height = screen_size()

    @property
    def width(self) -> int:
        """
        The width of the game area.
        """
        return self.__width

    @property
    def height(self) -> int:
        """
        The height of the game area.
        """
        return self.__height

    @property
    def root(self) -> GameObject:
        """
        Returns the root GameObject.
        """
        return self.__root

    @property
    def children(self) -> list[GameObject]:
        """
        Convenience method to get the children of the root GameObject.
        """
        return self.__root.children

    def add_child(self, child: GameObject) -> GameObject:
        """
        Convenience method to add a child to the root GameObject.
        """
        return self.__root.add_child(child)

    def remove_child(self, child: GameObject) -> GameObject:
        """
        Convenience method to remove a child from the root GameObject.
        """
        return self.__root.remove_child(child)

    def add_draw_func(self, func: Callable[[Any], None]):
        """
        Adds a custom draw function that is called before the root GameObject is drawn.
        """
        self.__draw_funcs.append(func)

    def add_update_func(self, func: Callable[[float], None]):
        """
        Adds a custom update function that is called before the root GameObject is updated.
        """
        self.__update_funcs.append(func)

    def draw(self, surface: Any):
        """
        Draws the entire GameObject hierarchy starting with the root GameObject and then the
        custom draw functions.

        The surface is passed down through all objects but does not need to be a Pygame
        surface, it can be any object you like provided it is compatible with the selected
        graphics driver.
        """
        self.__root.draw_hierarchy(surface)

        for draw_func in self.__draw_funcs:
            draw_func(surface)

    def update(self, dt: float):
        """
        Updates the entire GameObject hierarchy starting with the root GameObject and then
        the custom update functions.
        """
        self.__root.update_hierarchy(dt)

        for update_func in self.__update_funcs:
            update_func(dt)

    def terminate(self):
        """
        Terminates the application by destroying all objects and then delegating to the
        system module.
        """
        self.root.destroy()
        terminate()

    def run(self):
        """
        Runs the actual game at the desired resolution.
        """
        execute(self, self.__width, self.__height, self.background_color)
