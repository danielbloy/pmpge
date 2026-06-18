import validate.graphics.borders as borders
import validate.graphics.scaling as scaling
import validate.graphics.sprite_hierarchy as hierarchy
import validate.graphics.sprite_visibility as visibility
import validate.graphics.sprites as sprites
import validate.utils as utils

modules = [borders, scaling, sprites, visibility, hierarchy]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
