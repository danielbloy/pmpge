# Controller Driver

The controller driver is relatively simple in terms of expectations. It's primary
objective is to set the class variables on the `Controller` class in the `controller`
module by calling `Controller.update()`.

## Optional methods

### `init(game)`

Called once when the game first runs.

#### Parameters

* `game` - the Game object that is being executed

### `update(delta_time: float)`

Called once every update cycle before anything else.

#### Parameters

* `delta_time` - the time since update was last called, in fractions of a second.

### `deinit()`

Called once when the game finishes.
