# TODO: Provide environment information like screen width, height
import pmpge.environment as environment

__system = environment.import_driver('system')
run = __system.run
