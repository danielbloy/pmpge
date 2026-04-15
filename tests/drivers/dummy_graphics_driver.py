import time

loaded = time.monotonic_ns()

call_order = []
init_called = 0
update_called = 0
deinit_called = 0

width = None
height = None
screen_width = None
screen_height = None
screen_clear = None
background_colour = None
screen_draw = None


def init(w: int, h: int, sw: int, sh: int):
    global width, height, screen_width, screen_height
    width = w
    height = h
    screen_width = sw
    screen_height = sh
    global init_called
    init_called = time.monotonic_ns()
    call_order.append('init')


def clear(screen, bgc: tuple[int, int, int]):
    global screen_clear, background_colour
    background_colour = bgc
    screen_clear = screen
    call_order.append('clear')


def draw(screen):
    global screen_draw
    screen_draw = screen
    call_order.append('draw')


def update(dt):
    global update_called
    update_called = time.monotonic_ns()
    call_order.append('update')


def deinit():
    global deinit_called
    deinit_called = time.monotonic_ns()
    call_order.append('deinit')
