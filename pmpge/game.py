from collections.abc import Callable
from typing import Any

from pmpge.game_object import GameObject
from pmpge.system import run


class Game:
    """
    Game is the root of the GameObject hierarchy. It provides a simple way to manage the root
    GameObject as well as provide custom draw and update functions that are called after the
    root GameObject is drawn or updated.
    """

    def __init__(self, background_color: tuple[int, int, int] = (0, 0, 0)):
        self.background_color: tuple[int, int, int] = background_color
        self.__draw_funcs: list[Callable[[Any], None]] = []
        self.__update_funcs: list[Callable[[float], None]] = []
        self.__root = GameObject(name="root")

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

        The surface is passed down through all objects but does not need to be a Pygame surface. It
        can be any object you like provided it has a `fill()` method that accepts am RGB colour
        tuple.
        """
        surface.fill(self.background_color)

        self.__root.draw_hierarchy(surface)

        for draw_func in self.__draw_funcs:
            draw_func(surface)

    def update(self, dt: float):
        """
        Updates the entire GameObject hierarchy starting with the root GameObject and then the
        custom update functions.
        """
        self.__root.update_hierarchy(dt)

        for update_func in self.__update_funcs:
            update_func(dt)

    def run(self):
        """
        Runs the game.
        """
        run()
