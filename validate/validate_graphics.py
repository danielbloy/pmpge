import validate.graphics.borders as b
import validate.graphics.multiple_sprites as ms
import validate.graphics.scaling as gs
import validate.graphics.single_sprite as ss
import validate.graphics.sprite_hierarchy as sh
import validate.graphics.sprite_movement as sm
import validate.graphics.sprite_orbiting as so
import validate.graphics.sprite_visibility as sv
import validate.utils as utils

modules = [b, gs, ss, ms, sm, sv, sh, so]

# TODO: Small screen, add a graphic in each corner.

if utils.should_execute(__name__):
    utils.execute_modules(modules)
