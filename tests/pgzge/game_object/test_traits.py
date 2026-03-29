from dataclasses import dataclass
from typing import Any

import pytest

from pgzge.game_object import GameObject


@dataclass
class TraitWithJustProperties:
    my_int_property: int
    my_str_property: str


class TraitWithNothingToCopyAcross:
    """
    Nothing on this trait should be copied across to the GameObject.
    """

    def some_method(self):
        pass

    @property
    def pos(self) -> tuple[int, int]:
        return 0, 0

    @pos.setter
    def pos(self, pos: tuple[int, int]) -> None:
        pass


class TraitWithDrawHandler:
    def __init__(self):
        self.go = None
        self.surface = None
        self.count = 0

    def draw(self, surface: Any) -> None:
        self.go = self
        self.surface = surface
        self.count += 1


class TraitWithUpdateHandler:
    def __init__(self):
        self.go = None
        self.dt = None
        self.count = 0

    def update(self, dt: float) -> None:
        self.go = self
        self.dt = dt
        self.count += 1


class TraitWithActivatedHandler:
    def __init__(self):
        self.go = None
        self.count = 0

    def activated(self) -> None:
        self.go = self
        self.count += 1


class TraitWithDeactivatedHandler:
    def __init__(self):
        self.go = None
        self.count = 0

    def deactivated(self) -> None:
        self.go = self
        self.count += 1


class TraitWithDestroyedHandler:
    def __init__(self):
        self.go = None
        self.count = 0

    def destroyed(self) -> None:
        self.go = self
        self.count += 1


class TraitWithMergedHandler:
    def __init__(self):
        self.go = None
        self.count = 0

    def merged(self) -> None:
        self.go = self
        self.count += 1


class TraitWithEverything:
    def __init__(self):
        self.my_int_property: int = 27
        self.my_str_property: str = "some string"
        self.go = None
        self.surface = None
        self.dt = None
        self.called = []

    def draw(self, surface: Any) -> None:
        self.go = self
        self.surface = surface
        self.called.append("draw")

    def update(self, dt: float) -> None:
        self.go = self
        self.dt = dt
        self.called.append("update")

    def activated(self) -> None:
        self.go = self
        self.called.append("activated")

    def deactivated(self) -> None:
        self.go = self
        self.called.append("deactivated")

    def destroyed(self) -> None:
        self.go = self
        self.called.append("destroyed")

    def merged(self) -> None:
        self.go = self
        self.called.append("merged")


# noinspection PyUnresolvedReferences
def test_properties_are_copied_across():
    """
    Validates that properties are copied across to the GameObject.
    """
    go = GameObject()
    go.apply_trait(TraitWithJustProperties(13, "a string"))
    assert hasattr(go, 'my_int_property')
    assert hasattr(go, 'my_str_property')
    assert go.my_int_property == 13
    assert go.my_str_property == "a string"


# noinspection PyUnresolvedReferences
def test_methods_are_not_copied_across():
    """
    Validates that unexpected methods are NOT copied to the GameObject
    """
    go = GameObject()
    go.apply_trait(TraitWithNothingToCopyAcross)
    assert not hasattr(go, 'some_method')
    assert not hasattr(go, 'pos')

    with pytest.raises(AttributeError):
        a = go.pos

    with pytest.raises(AttributeError):
        go.some_method()


# noinspection PyUnresolvedReferences
def test_draw_handler_copied_across():
    """
    Validates that draw() is copied across to the GameObject as a handler.
    """
    go = GameObject()
    go.apply_trait(TraitWithDrawHandler)
    assert go.go is None
    assert go.surface is None
    assert go.count == 0

    go.draw_hierarchy("surface")

    assert go.go == go
    assert go.surface == "surface"
    assert go.count == 1


# noinspection PyUnresolvedReferences
def test_update_handler_copied_across():
    """
    Validates that update() is copied across to the GameObject as a handler.
    """
    go = GameObject()
    go.apply_trait(TraitWithUpdateHandler)
    assert go.go is None
    assert go.dt is None
    assert go.count == 0

    go.update_hierarchy(1.2)

    assert go.go == go
    assert go.dt == 1.2
    assert go.count == 1


# noinspection PyUnresolvedReferences
def test_activated_handler_copied_across():
    """
    Validates that activated() is copied across to the GameObject as a handler.
    """
    go = GameObject(active=False)
    go.apply_trait(TraitWithActivatedHandler)
    assert go.go is None
    assert go.count == 0

    go.activate()

    assert go.go == go
    assert go.count == 1

    go = GameObject(active=True)
    go.apply_trait(TraitWithActivatedHandler)
    assert go.go == go
    assert go.count == 1


# noinspection PyUnresolvedReferences
def test_deactivated_handler_copied_across():
    """
    Validates that deactivated() is copied across to the GameObject as a handler.
    """
    go = GameObject(active=True)
    go.apply_trait(TraitWithDeactivatedHandler)
    assert go.go is None
    assert go.count == 0

    go.deactivate()

    assert go.go == go
    assert go.count == 1

    go = GameObject(active=False)
    go.apply_trait(TraitWithDeactivatedHandler)
    assert go.go == go
    assert go.count == 1


# noinspection PyUnresolvedReferences
def test_destroyed_handler_copied_across():
    """
    Validates that destroyed() is copied across to the GameObject as a handler.
    """
    go = GameObject()
    go.apply_trait(TraitWithDestroyedHandler)
    assert go.go is None
    assert go.count == 0

    go.destroy()

    assert go.go == go
    assert go.count == 1


# noinspection PyUnresolvedReferences
def test_merged_handler_called():
    """
    Validates that merged() is called.
    """
    go = GameObject()
    go.apply_trait(TraitWithMergedHandler)
    assert go.go == go
    assert go.count == 1


# noinspection PyUnresolvedReferences
def test_all_handlers_copied_across():
    """
    Validates that all functions are copied across to the GameObject.
    """
    go = GameObject()
    go.apply_trait(TraitWithEverything)
    assert go.go == go
    assert go.surface is None
    assert go.dt is None
    assert go.called == ["activated", "merged"]

    go.reset()
    assert go.go == go
    assert go.surface is None
    assert go.dt is None
    assert go.called == ["activated", "merged", "deactivated", "activated"]

    go.draw_hierarchy("surface")
    assert go.go == go
    assert go.surface == "surface"
    assert go.dt is None
    assert go.called == ["activated", "merged", "deactivated", "activated", "draw"]

    go.update_hierarchy(1.2)
    assert go.go == go
    assert go.surface == "surface"
    assert go.dt == 1.2
    assert go.called == ["activated", "merged", "deactivated", "activated", "draw", "update"]

    go.destroy()
    assert go.go == go
    assert go.surface == "surface"
    assert go.dt == 1.2
    assert go.called == ["activated", "merged", "deactivated", "activated", "draw", "update", "deactivated",
                         "destroyed"]


# noinspection PyUnresolvedReferences
def test_add_multiple_traits_copied_across_different_handlers():
    """
    Validates that draw() and update() are copied across to the GameObject as a handler.
    """
    go = GameObject()
    go.apply_trait(TraitWithDrawHandler)
    go.apply_trait(TraitWithUpdateHandler)
    assert go.go is None
    assert go.surface is None
    assert go.dt is None
    assert go.count == 0

    go.draw_hierarchy("surface")

    assert go.go == go
    assert go.surface == "surface"
    assert go.count == 1

    go.update_hierarchy(1.2)

    assert go.go == go
    assert go.surface == "surface"
    assert go.dt == 1.2
    assert go.count == 2


# noinspection PyUnresolvedReferences
def test_add_multiple_traits_copied_across_same_handlers():
    """
    Validates that draw() and update() are copied across to the GameObject as a handler.
    """
    go = GameObject()
    go.apply_trait(TraitWithDrawHandler)
    go.apply_trait(TraitWithDrawHandler)
    go.apply_trait(TraitWithUpdateHandler)
    go.apply_trait(TraitWithUpdateHandler)
    go.apply_trait(TraitWithUpdateHandler)
    assert go.go is None
    assert go.surface is None
    assert go.dt is None
    assert go.count == 0

    go.draw_hierarchy("surface")

    assert go.go == go
    assert go.surface == "surface"
    assert go.count == 2

    go.update_hierarchy(1.2)

    assert go.go == go
    assert go.surface == "surface"
    assert go.dt == 1.2
    assert go.count == 5


def test_trait_class_fails_when_constructor_has_parameters():
    """
    When using the class type as a trait, it must have a parameterless
    constructor, otherwise the constructor will fail.
    """
    go = GameObject()
    with pytest.raises(TypeError):
        go.apply_trait(TraitWithJustProperties)

    with pytest.raises(TypeError):
        GameObject(TraitWithJustProperties)
