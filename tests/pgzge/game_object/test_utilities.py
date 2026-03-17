from pgzge.core import GameObject


class TestHandlers:
    """
    Utility class to help track which handlers are called. This also provides a useful way
    to create a GameObject with the handlers already set.
    """

    def __init__(self):
        self.called_order = []
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
        self.called_order = []
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
        self.called_order.append("draw")
        self.draw_called = (obj, surface)
        self.draw_called_count += 1

    def update(self, obj, dt):
        self.called_order.append("update")
        self.update_called = (obj, dt)
        self.update_called_count += 1

    def activate(self, obj):
        self.called_order.append("activate")
        self.activate_called = obj
        self.activate_called_count += 1

    def deactivate(self, obj):
        self.called_order.append("deactivate")
        self.deactivate_called = obj
        self.deactivate_called_count += 1

    def destroy(self, obj):
        self.called_order.append("destroy")
        self.destroy_called = obj
        self.destroy_called_count += 1

    def validate(self,
                 called_order=None,  # We only validate this if specified
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
        if called_order is not None:
            assert self.called_order == called_order

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

    def create_game_object(self):
        """Create a game object with default settings but with handlers set."""
        go = GameObject(
            draw_handler=self.draw,
            update_handler=self.update,
            activate_handler=self.activate,
            deactivate_handler=self.deactivate,
            destroy_handler=self.destroy)
        return go
