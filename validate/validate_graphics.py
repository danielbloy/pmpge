import validate_device.graphics.borders as egb
import validate_device.graphics.multiple_sprites as ems
import validate_device.graphics.scaling as egs
import validate_device.graphics.single_sprite as ess
import validate_device.graphics.sprite_hierarchy as esv
import validate_device.graphics.sprite_movement as esm
import validate_device.graphics.sprite_orbiting as ego
import validate_device.graphics.sprite_visibility as esh
import validate_device.utils as utils

modules = [egb, egs, ess, ems, esm, esv, esh, ego]

# TODO: Small screen, add a graphic in each corner.

if utils.should_execute(__name__):
    utils.execute_modules(modules)
