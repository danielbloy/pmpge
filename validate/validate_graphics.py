import validate.graphics.borders as borders
import validate.graphics.scaling as scaling
import validate.graphics.sprite_hierarchy as sh
import validate.graphics.sprite_visibility as sprite_visibility
import validate.graphics.sprites as sprites
import validate.utils as utils

modules = [borders, scaling, sprites, sprite_visibility, sh]

# TODO: Small screen, add a graphic in each corner.
# TODO: Rework the hierarchy drawing example.

if utils.should_execute(__name__):
    utils.execute_modules(modules)
