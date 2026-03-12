class TestHandlers:
    """
    Utility class to help track which handlers are called.
    """

    def __init__(self):
        self.draw_called = None
        self.draw_Called_count = 0
        self.update_called = None
        self.update_Called_count = 0
        self.activate_called = None
        self.activate_Called_count = 0
        self.deactivate_called = None
        self.deactivate_Called_count = 0
        self.destroy_called = None
        self.destroy_Called_count = 0

    def reset(self):
        self.draw_called = None
        self.draw_Called_count = 0
        self.update_called = None
        self.update_Called_count = 0
        self.activate_called = None
        self.activate_Called_count = 0
        self.deactivate_called = None
        self.deactivate_Called_count = 0
        self.destroy_called = None
        self.destroy_Called_count = 0

    def draw(self, obj, surface):
        self.draw_called = (obj, surface)
        self.draw_Called_count += 1

    def update(self, obj, dt):
        self.update_called = (obj, dt)
        self.update_Called_count += 1

    def activate(self, obj):
        self.activate_called = obj
        self.activate_Called_count += 1

    def deactivate(self, obj):
        self.deactivate_called = obj
        self.deactivate_Called_count += 1

    def destroy(self, obj):
        self.destroy_called = obj
        self.destroy_Called_count += 1
