import validate.graphics.borders as egb
import validate.graphics.multiple_sprites as ems
import validate.graphics.scaling as egs
import validate.graphics.single_sprite as ess
import validate.graphics.sprite_hierarchy as esv
import validate.graphics.sprite_movement as esm
import validate.graphics.sprite_orbiting as ego
import validate.graphics.sprite_visibility as esh
import validate.utils as utils

modules = [egb, egs, ess, ems, esm, esv, esh, ego]

# TODO: Small screen, add a graphic in each corner.

if utils.should_execute(__name__):
    utils.execute_modules(modules)
