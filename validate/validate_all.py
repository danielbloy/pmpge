# This script runs all the validation tests. It is a convenient way to
# test a large subset of the functionality on a single device.
#
import validate.controller.move_sprite as cfms
import validate.engine.game_objects_with_traits as egot
import validate.engine.hierarchy_with_traits as ehwt
import validate.engine.just_game_objects as ejgo
import validate.engine.trivial_game as etg
import validate.graphics.borders as gb
import validate.graphics.multiple_sprites as gms
import validate.graphics.scaling as gs
import validate.graphics.single_sprite as gss
import validate.graphics.sprite_hierarchy as gsh
import validate.graphics.sprite_movement as gsm
import validate.graphics.sprite_orbiting as gso
import validate.graphics.sprite_visibility as gsv
import validate.performance.baseline as pb
import validate.performance.baseline_with_graphics as pbwg
import validate.performance.baseline_with_graphics_small_display as pbsd
import validate.performance.huge_hierarchy as phh
import validate.utils as utils

modules = [etg, ejgo, egot, ehwt, cfms, pb, pbwg, pbsd, phh, gb, gs, gss, gms, gsm, gsv, gsh, gso]

if utils.should_execute(__name__):
    utils.execute_modules(modules)
