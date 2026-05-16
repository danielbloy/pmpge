import tests.validate_device.utils as utils
import tests.validate_device.validate_a_game as a
import tests.validate_device.validate_b_game_object as b
import tests.validate_device.validate_c_hierarchy as c
import tests.validate_device.validate_c_huge_hierarchy as ch
import tests.validate_device.validate_d_traits as d
import tests.validate_device.validate_d_traits_simple as ds
import tests.validate_device.validate_e_graphics_borders as egb
import tests.validate_device.validate_e_graphics_multiple_sprites as ems
import tests.validate_device.validate_e_graphics_scaling as egs
import tests.validate_device.validate_e_graphics_single_sprite as ess
import tests.validate_device.validate_e_graphics_sprite_hierarchy as esv
import tests.validate_device.validate_e_graphics_sprite_movement as esm
import tests.validate_device.validate_e_graphics_sprite_orbiting as ego
import tests.validate_device.validate_e_graphics_sprite_visibility as esh

modules = [a, b, c, ch, ds, d, egb, egs, ess, ems, esm, esv, esh, ego]


def execute():
    for module in modules:
        try:
            if utils.is_running_on_desktop():
                from types import ModuleType
                from pgzero.game import PGZeroGame
                PGZeroGame(module).reinit_screen()

            print("Executing module {}".format(module))

            # This allows the validate script to override the default screen size.
            screen_width, screen_height = 160, 120
            if hasattr(module, "SCREEN_WIDTH"):
                screen_width = module.SCREEN_WIDTH
            if hasattr(module, "SCREEN_HEIGHT"):
                screen_height = module.SCREEN_HEIGHT

            utils.execute(module.setup, screen_width=screen_width, screen_height=screen_height)
            del module

        except MemoryError:
            print("Memory Error")


if utils.should_execute(__name__):
    execute()
