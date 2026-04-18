import tests.validate_device.validate_a_core as a
from tests.validate_device.memory import report_memory_usage, report_memory_usage_and_free

modules = [a]


def execute():
    report_memory_usage()
    for module in modules:
        print("Executing module {}".format(module))
        module.execute()
        report_memory_usage_and_free()
        del module


if __name__ == '__main__':
    execute()
