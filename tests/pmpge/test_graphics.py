# TODO: Add tests

# We are extracting out the graphics rendering pipeline from being
# directly controlled by GameObject to support different rendering
# strategies based on the target platform. This also allows for
# more tergetted optimisation.

# TODO: Game
# TODO: Need a build() render_pipeline - basically draw_hierarchy()
#       returning a list of objects to render
# TODO: Need a rebuild() render_pipeline
