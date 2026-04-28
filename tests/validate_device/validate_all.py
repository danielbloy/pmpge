import tests.validate_device.utils as utils
import tests.validate_device.validate_a_game as a
import tests.validate_device.validate_b_game_object as b
import tests.validate_device.validate_c_hierarchy as c
import tests.validate_device.validate_c_huge_hierarchy as ch
import tests.validate_device.validate_d_traits as d
import tests.validate_device.validate_d_traits_simple as ds
import tests.validate_device.validate_e_graphics_multiple_sprites as ems
import tests.validate_device.validate_e_graphics_single_sprite as ess
import tests.validate_device.validate_e_graphics_sprite_movement as esm
import tests.validate_device.validate_e_graphics_sprite_visibility as esv

modules = [a, b, c, ch, ds, d, ess, ems, esm, esv]


def execute():
    for module in modules:
        try:
            if utils.is_running_on_desktop():
                from types import ModuleType
                from pgzero.game import PGZeroGame
                PGZeroGame(module).reinit_screen()
            print("Executing module {}".format(module))
            utils.execute(module.setup)
            del module
        except MemoryError:
            print("Memory Error")


if utils.should_execute(__name__):
    execute()

# TODO: Add a test to validate display Z-order
