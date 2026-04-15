import time

loaded = time.monotonic_ns()

call_order = []
init_called = 0
update_called = 0
deinit_called = 0


def init():
    global init_called
    init_called = time.monotonic_ns()
    call_order.append('init')


def update(dt):
    global update_called
    update_called = time.monotonic_ns()
    call_order.append('update')


def deinit():
    global deinit_called
    deinit_called = time.monotonic_ns()
    call_order.append('deinit')
