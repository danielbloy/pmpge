from typing import Any


# TODO: Explain the difference between traits and merging.
# TODO: Strictly speaking the merge does not need to be in sprite and is generic. It could
#       even go at the GameObject level. However, let's keep it separate from GO to avoid
#       GO becoming too big and complex. I also can't think of a major case for doing this
#       at the GO level.
# TODO: Add size, width, height, topleft, topright etc. properties
# TODO: Add bounding box property

# TODO: Explain what a trait is and how it works.

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
