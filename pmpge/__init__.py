import pmpge.environment as environment

# Initialise the device next to allow it to perform any setup.
__device = environment.import_driver('device')

environment.report()
