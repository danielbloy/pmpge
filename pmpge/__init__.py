import pmpge.environment as environment

# Initialise the device next to allow it to perform any setup.
__device = environment.import_driver('device')

# Now we initialise each of the other subsystems.
environment.import_driver('platform')
environment.import_driver('graphics')
environment.import_driver('controller')
environment.import_driver('sound')

environment.report()
