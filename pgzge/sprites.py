from collections.abc import Callable
from typing import Self, Any

from pgzero.keyboard import Keyboard
from pgzero.loaders import images

from pgzge.core import GameObject

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)


# TODO: Sprites still needs some refinement to simplify their use, especially Kinds.

class Sprite(GameObject):

    def merge(self, other: Any) -> Self:
        """
        Merge the properties and handlers of another object into a GameObject. It will
        not merge across methods or property getter and setters. For that you will
        need to define a subclass of GameObject or create one dynamically via SpriteKinds.
        """
        self.__dict__.update(other.__dict__)

        cls = other.__class__

        if hasattr(cls, 'draw'):
            self.add_draw_handler(cls.draw)

        if hasattr(cls, 'update'):
            self.add_update_handler(cls.update)

        if hasattr(cls, 'activated'):
            self.add_activate_handler(cls.activated)

        if hasattr(cls, 'deactivated'):
            self.add_deactivate_handler(cls.deactivated)

        if hasattr(cls, 'destroyed'):
            self.add_destroy_handler(cls.destroyed)

        # Trigger activate and/or deactivate handlers on the combined game_object if they exist.
        if hasattr(cls, 'activated') and self.active:
            cls.activated(self)

        if hasattr(cls, 'deactivated') and not self.active:
            cls.deactivated(self)

        # Finally trigger the merge handler.
        if hasattr(cls, 'merged'):
            cls.merged(self)

        return self


def new_kind(name: str, *traits_classes: type) -> type:
    return type(name, (Sprite, Position, *traits_classes), {})


def new_sprite(kind: type,
               x: float, y: float,
               *traits,
               name: str | None = None,
               active: bool = True,
               enabled: bool = True,
               visible: bool = True,
               children: list[GameObject] = None
               ) -> Sprite:
    """
    """
    sprite = kind.__new__(kind)

    # We don't use merge here because game_object is the basis of the sprite.
    base = GameObject(
        name=name,
        active=active,
        enabled=enabled,
        visible=visible,
        children=children
    )
    sprite.__dict__.update(base.__dict__)

    sprite.merge(Position(x, y))

    for trait in traits:
        sprite.merge(trait)

    return sprite


class Kinds:
    def __init__(self):
        self.types: dict[str, type] = {}

    def new(self, name: str, *traits_classes: type) -> type:
        if name in self.types:
            raise ValueError(f"Sprite kind '{name}' already exists.")

        self.types[name] = new_kind(name, *traits_classes)
        return self.types[name]

    def __contains__(self, item) -> bool:
        return item in self.types

    def __getitem__(self, item: str) -> type:
        return self.get(item)

    def __iter__(self):
        return iter(self.types.items())

    def get(self, name: str, *traits_classes: type) -> type:
        if name in self.types:
            return self.types[name]

        return self.new(name, *traits_classes)


class Sprites:
    def __init__(self, kinds: Kinds = Kinds()):
        self.kinds = kinds
        self.sprites: dict[str, list[GameObject]] = {}

    def new(self,
            kind: str,
            x: float, y: float,
            *traits,
            name: str | None = None,
            active: bool = True,
            enabled: bool = True,
            visible: bool = True,
            children: list[GameObject] = None
            ) -> Sprite:
        """
        """
        traits_classes = [trait.__class__ for trait in traits]
        kind_type = self.kinds.get(kind, *traits_classes)
        sprite = new_sprite(
            kind_type,
            x, y,
            *traits,
            name=name,
            active=active,
            enabled=enabled,
            visible=visible,
            children=children)

        sprite.add_destroy_handler(lambda obj: self.sprites[kind].remove(sprite))
        self.sprites.get(kind, []).append(sprite)

        return sprite


# TODO: Should all the classes below be postfixed with Mixin?

class Position:
    def __init__(self, x, y: float):
        self.x: float = x
        self.y: float = y

    @property
    def position(self) -> tuple[float, float]:
        return self.x, self.y

    @position.setter
    def position(self, position: tuple[float, float]) -> None:
        self.x = position[0]
        self.y = position[1]

    @property
    def pos(self) -> tuple[float, float]:
        return self.x, self.y

    @pos.setter
    def pos(self, pos: tuple[float, float]) -> None:
        self.x = pos[0]
        self.y = pos[1]


class RelativeToParent:
    def __init__(self, offset_x, offset_y: int):
        self.offset_x: int = offset_x
        self.offset_y: int = offset_y

    def update(self, dt: int):
        if self.parent:
            self.x = self.parent.x + self.offset_x
            self.y = self.parent.y + self.offset_y
        else:
            self.x = self.offset_x
            self.y = self.offset_y


class Motion:
    def __init__(self, vx, vy: int):
        self.vx: int = vx
        self.vy: int = vy

    def update(self, dt: float):
        self.x += dt * self.vx
        self.y += dt * self.vy


class MoveWithKeyboard:
    def __init__(self, vx, vy: int, keyboard: Keyboard):
        self.vx: int = vx
        self.vy: int = vy
        self.keyboard: Keyboard = keyboard

    def update(self, dt: float):
        new_pos = self.pos
        keyboard = self.keyboard
        if keyboard.a or keyboard.left:
            new_pos = (new_pos[0] - (self.vx * dt), new_pos[1])
        elif keyboard.d or keyboard.right:
            new_pos = (new_pos[0] + (self.vx * dt), new_pos[1])

        self.position = new_pos


class StayInBounds:
    def __init__(self, min_x, min_y, max_x, max_y: int):
        self.min_x: int = min_x
        self.max_x: int = max_x
        self.min_y: int = min_y
        self.max_y: int = max_y

    def update(self, dt: float):
        if self.x < self.min_x:
            self.x = self.min_x
        elif self.x > self.max_x:
            self.x = self.max_x

        if self.y < self.min_y:
            self.y = self.min_y
        elif self.y > self.max_y:
            self.y = self.max_y


class Lifetime:
    def __init__(self, lifetime: float = None):
        self.lifetime = lifetime

    def update(self, dt: float):
        if self.lifetime:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.destroy = True
                return


class DrawImage:
    """
    This works without requiring properties.
    """

    def __init__(self, image: str):
        self._surface = None
        self._offset_x = None
        self._offset_y = None

        self._image = None
        self.image = image

    def draw(self, surface: Any):
        if self.image != self._image:
            self._image = self.image
            self._surface = images.load(self.image)
            self._offset_x = self._surface.get_width() / 2
            self._offset_y = self._surface.get_height() / 2

        surface.blit(self._surface, (self.x - self._offset_x, self.y - self._offset_y))


class DrawText:
    def __init__(self,
                 text: str | Callable[[GameObject], str],
                 colour: tuple[int, int, int] = WHITE,
                 background: tuple[int, int, int] | None = None,
                 fontname: str | None = None,
                 fontsize: int = 16):
        self.text = text
        self.colour = colour
        self.background = background
        self.fontname = fontname
        self.fontsize = fontsize

    def draw(self, surface: Any):
        text = self.text
        if not isinstance(text, str):
            text = self.text(self)

        surface.draw.text(
            text,
            bottomleft=self.pos,
            color=self.colour,
            background=self.background,
            fontname=self.fontname,
            fontsize=self.fontsize)
