# Graphics Driver

## Optional methods

### `init(width, height, screen_width, screen_height, background_colour)`

Called once when the game first runs.

#### Parameters

* `width` - the width of the game in pixels.
* `height` - the height of the game in pixels.
* `screen_width` - the width of the screen in pixels.
* `screen_height` - the height of the screen in pixels.
* `background_colour` - the default colour of the background in RGB format.

### `update(delta_time: float)`

Called once every update cycle before anything else.

#### Parameters

* `delta_time` - the time since update was last called, in fractions of a second.

### `deinit()`

Called once when the game finishes.

## Mandatory methods

A graphics driver must implement the following mandatory methods:

### `clear(surface)`

Called once per frame. Called before any other display operations.

#### Parameters

* `surface` - an implementation dependent parameter representing the visual
  surface to draw to. For Pygame Zero this will be the `screen` variable. For
  microcontrollers this will be None.

### `draw(surface)`

Called once per frame and passed a surface object that is implementation-dependent.
Called after the game is drawn to the screen to allow for any final operations such
as scaling or flipping.

#### Parameters

* `surface` - an implementation dependent parameter representing the visual
  surface to draw to. For Pgzero this will be the `screen` variable. For
  microcontrollers this will be None.

## Mandatory classes

A graphics driver must implement the following mandatory classes:

### `ImageLoader`

# TODO: Document ImageLoader.
