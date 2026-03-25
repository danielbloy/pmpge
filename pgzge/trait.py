from typing import Any

from pgzge.core import GameObject


# TODO: Explain the difference between traits and merging.
# TODO: Strictly speaking the merge does not need to be in sprite and is generic. It could
#       even go at the GameObject level. However, let's keep it separate from GO to avoid
#       GO becoming too big and complex. I also can't think of a major case for doing this
#       at the GO level.


# TODO: Explain what a trait is and how it works.

class GameObjectWithTraits(GameObject):
    def add_trait(self, trait: Any) -> None:
        merge(self, trait)


def new_kind(name: str, *traits_classes: type) -> type:
    return type(name, (GameObjectWithTraits, *traits_classes), {})


# TODO: Replace kind with some kind finder.
def new_object_with_traits(base: GameObject, *traits, kind: type = None) -> GameObjectWithTraits:
    """
    """
    print(f"traits: {traits}")  # TODO: Remove
    traits_classes = [trait.__class__ for trait in traits]
    kind = kind if kind else new_kind(base.name if base.name else "", *traits_classes)
    result = kind.__new__(kind)

    # We don't use merge here because game_object is the basis of the sprite.
    result.__dict__.update(base.__dict__)

    for trait in traits:
        merge(result, trait)

    return result


def merge(base, trait: Any) -> Any:
    """
    Merge the properties and handlers of another object into a GameObject. It will
    not merge across methods or property getter and setters. For that you will
    need to define a subclass of GameObject or create one dynamically via SpriteKinds.
    """
    base.__dict__.update(trait.__dict__)

    cls = trait.__class__

    if hasattr(cls, 'draw'):
        base.add_draw_handler(cls.draw)

    if hasattr(cls, 'update'):
        base.add_update_handler(cls.update)

    if hasattr(cls, 'activated'):
        base.add_activate_handler(cls.activated)

    if hasattr(cls, 'deactivated'):
        base.add_deactivate_handler(cls.deactivated)

    if hasattr(cls, 'destroyed'):
        base.add_destroy_handler(cls.destroyed)

    # Trigger activate and/or deactivate handlers on the combined game_object if they exist.
    if hasattr(cls, 'activated') and base.active:
        cls.activated(base)

    if hasattr(cls, 'deactivated') and not base.active:
        cls.deactivated(base)

    # Finally trigger the merge handler.
    if hasattr(cls, 'merged'):
        cls.merged(base)

    return base
