import tests.validate_device.utils as utils
import tests.validate_device.validate_a_game as a
import tests.validate_device.validate_b_game_object as b
import tests.validate_device.validate_c_hierarchy as c
import tests.validate_device.validate_c_huge_hierarchy as ch
import tests.validate_device.validate_d_traits as d
import tests.validate_device.validate_d_traits_simple as ds

modules = [a, b, c, ch, ds, d]


def execute():
    for module in modules:
        try:
            print("Executing module {}".format(module))
            utils.execute(module.setup)
            del module
        except MemoryError:
            print("Memory Error")


if utils.should_execute(__name__):
    execute()
