import pmpge.environment as environment

__system = environment.import_driver('system')
initialise = __system.initialise
execute = __system.execute
terminate = __system.terminate
