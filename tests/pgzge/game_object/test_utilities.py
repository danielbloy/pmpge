class TestHandlers:
    """
    Utility class to help track which handlers are called.
    """

    def __init__(self):
        self.draw_called = None
        self.draw_called_count = 0
        self.update_called = None
        self.update_called_count = 0
        self.activate_called = None
        self.activate_called_count = 0
        self.deactivate_called = None
        self.deactivate_called_count = 0
        self.destroy_called = None
        self.destroy_called_count = 0

    def reset(self):
        self.draw_called = None
        self.draw_called_count = 0
        self.update_called = None
        self.update_called_count = 0
        self.activate_called = None
        self.activate_called_count = 0
        self.deactivate_called = None
        self.deactivate_called_count = 0
        self.destroy_called = None
        self.destroy_called_count = 0

    def draw(self, obj, surface):
        self.draw_called = (obj, surface)
        self.draw_called_count += 1

    def update(self, obj, dt):
        self.update_called = (obj, dt)
        self.update_called_count += 1

    def activate(self, obj):
        self.activate_called = obj
        self.activate_called_count += 1

    def deactivate(self, obj):
        self.deactivate_called = obj
        self.deactivate_called_count += 1

    def destroy(self, obj):
        self.destroy_called = obj
        self.destroy_called_count += 1

    def validate(self,
                 draw=None,
                 draw_count=0,
                 update=None,
                 update_count=0,
                 activate=None,
                 activate_count=0,
                 deactivate=None,
                 deactivate_count=0,
                 destroy=None,
                 destroy_count=0):
        assert self.draw_called == draw
        assert self.draw_called_count == draw_count
        assert self.update_called == update
        assert self.update_called_count == update_count
        assert self.activate_called == activate
        assert self.activate_called_count == activate_count
        assert self.deactivate_called == deactivate
        assert self.deactivate_called_count == deactivate_count
        assert self.destroy_called == destroy
        assert self.destroy_called_count == destroy_count
