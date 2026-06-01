import tests.validate_device.graphics.borders as egb
import tests.validate_device.graphics.multiple_sprites as ems
import tests.validate_device.graphics.scaling as egs
import tests.validate_device.graphics.single_sprite as ess
import tests.validate_device.graphics.sprite_hierarchy as esv
import tests.validate_device.graphics.sprite_movement as esm
import tests.validate_device.graphics.sprite_orbiting as ego
import tests.validate_device.graphics.sprite_visibility as esh
import tests.validate_device.utils as utils

modules = [egb, egs, ess, ems, esm, esv, esh, ego]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
