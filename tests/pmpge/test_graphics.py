# TODO: Add tests


# We are extracting out the graphics rendering pipeline from being
# directly controlled by GameObject to support different rendering
# strategies based on the target platform. This also allows for
# more tergetted optimisation.

# TODO: Game
# TODO: Need a build() render_pipeline - basically draw_hierarchy()
#       returning a list of objects to render
# TODO: Need a rebuild() render_pipeline

# TODO: A GameObject needs:
# * A Renderer(). The Renderer does not necessarily need to be an instance per GameObject
# * A resource. This is easy for images and they can be shared.
# * The Renderer needs access to GameObject() to get things like x, y co-ordinates
# * The renderer should be updated(), certainly notified if something changes, though
#   that is highly likely most of the time.
#
# * The information the renderer will need is:
#   x, y, visible, asset/resource
#
# * The render pipeline needs to know when parent/child relationships change as this
#   affects the order within which the objects are drawn.
# * The render pipeline needs to know when objects are created/destroyed as the
#   corresponding objects in the render pipeline will need to be added or removed.
