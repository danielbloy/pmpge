import pmpge.environment as environment

__platform = environment.import_driver('platform')
initialise = __platform.initialise
execute = __platform.execute
terminate = __platform.terminate
