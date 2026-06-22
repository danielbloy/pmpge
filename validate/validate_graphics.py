import validate.graphics.borders as borders
import validate.graphics.scaling as scaling
import validate.graphics.sprites as sprites
import validate.graphics.visibility as visibility
import validate.graphics.z_order as z_order
import validate.utils as utils

# TODO: Add a test on transparency

modules = [borders, scaling, sprites, visibility, z_order]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
