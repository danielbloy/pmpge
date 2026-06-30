import validate.graphics.borders as borders
import validate.graphics.scaling as scaling
import validate.graphics.sprites as sprites
import validate.graphics.transparency as transparency
import validate.graphics.visibility as visibility
import validate.graphics.z_order as z_order
import validate.utils as utils

modules = [borders, scaling, sprites, visibility, transparency, z_order]
modules = [transparency]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
