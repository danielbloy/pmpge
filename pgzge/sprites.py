from pgzge.core import GameObject
from pgzge.trait import merge
from pgzge.traits.position import Position


# TODO: Sprites still needs some refinement to simplify their use, especially Kinds.

class Sprite(GameObject):
    pass


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

    merge(sprite, Position(x, y))

    for trait in traits:
        merge(sprite, trait)

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
    """
    Sprites have position and are made up of mixins to provide additional functionality.
    """

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
