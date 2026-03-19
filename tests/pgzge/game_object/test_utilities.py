from typing import Self

from pgzge.core import GameObject


class TestHandlers:
    """
    Utility class to help track which handlers are called. This also provides a useful way
    to create a GameObject with the handlers already set.
    """

    def __init__(self, shared_called_order=None):
        # An optional shared list where we post all events. Useful for checking order of invocation
        # within a hierarchy.
        self.shared_called_order = shared_called_order

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
        if self.shared_called_order is not None:
            self.shared_called_order.append(f"draw {obj.name}")
        self.called_order.append("draw")
        self.draw_called = (obj, surface)
        self.draw_called_count += 1

    def update(self, obj, dt):
        if self.shared_called_order is not None:
            self.shared_called_order.append(f"update {obj.name}")
        self.called_order.append("update")
        self.update_called = (obj, dt)
        self.update_called_count += 1

    def activate(self, obj):
        if self.shared_called_order is not None:
            self.shared_called_order.append(f"activate {obj.name}")
        self.called_order.append("activate")
        self.activate_called = obj
        self.activate_called_count += 1

    def deactivate(self, obj):
        if self.shared_called_order is not None:
            self.shared_called_order.append(f"deactivate {obj.name}")
        self.called_order.append("deactivate")
        self.deactivate_called = obj
        self.deactivate_called_count += 1

    def destroy(self, obj):
        if self.shared_called_order is not None:
            self.shared_called_order.append(f"destroy {obj.name}")
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
        """
        Validate that the handlers were called the expected number of times..
        """
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

    def create_game_object(self, name=None):
        """
        Create a game object with default settings but with name and handlers set.
        """
        go = GameObject(
            name=name,
            draw_handler=self.draw,
            update_handler=self.update,
            activate_handler=self.activate,
            deactivate_handler=self.deactivate,
            destroy_handler=self.destroy)
        return go


class TestHierarchy:
    class Item:
        """
        Simple data class to hold a GameObject and its handler object.
        """

        def __init__(self, name: str, called_order: list[str]):
            self.handlers: TestHandlers = TestHandlers(shared_called_order=called_order)
            self.go: GameObject = self.handlers.create_game_object(name=name)

    """
    This class is used to provide details of a GameObject hierarchy for tests.
    """

    def __init__(self, name: str):
        self.called_order = []
        self.parent = TestHierarchy.Item(name, self.called_order)
        self.children = []
        self.grandchildren = []
        self.everyone = [self.parent]

    def reset(self):
        """
        Resets all GameObject handler tracking in the hierarchy.
        """
        self.called_order.clear()
        for item in self.everyone:
            item.handlers.reset()

    def add_child(self, name: str) -> Self:
        """
        Adds a child GameObject to the hierarchy.
        """
        child = TestHierarchy.Item(name, self.called_order)
        self.children.append(child)
        self.everyone.append(child)
        self.parent.go.add_child(child.go)
        return self

    def validate_properties(self, active=None, alive=None):
        """
        Validates that all items in the hierarchy have the same value for the specified property.
        """
        for item in self.everyone:
            if active is not None:
                assert item.go.active == active

            if alive is not None:
                assert item.go.alive == alive

    def validate_called_order(self,
                              expected_handler_order: list[str],
                              reverse=False,
                              interlace=False,
                              debug=False):
        """
        Validates that the handlers were all invoked in the expected order.

        If reverse is True, we reverse the expected order of the items in the hierarchy for
        call order; typically used for testing the order of destruction which is done in reverse.

        If interlace is false we expect all GameObjects to have the first handler invoked followed
        by all GameObjects to have the second handler invoked and so on. If interlace is True, we
        expect all GameObjects to have each handler invoked in turn followed by the next GameObject
        having each handler invoked in turn.
        """

        if debug:
            print()
            print("Expected called order:")
            print(expected_handler_order)
            print()
            print("Hierarchy:")
            for item in self.everyone:
                print(f"  {item.go.name} - {item.handlers.called_order}")
            print()

        # First make sure all GameObjects have the expected handler
        for item in self.everyone:
            assert item.handlers.called_order == expected_handler_order

        # Now make sure the handlers were called in the correct order.
        expected_shared_called_order = []
        items = self.everyone if not reverse else self.grandchildren + self.children + [self.parent]

        if interlace:
            for item in items:
                calls = [f"{handler} {item.go.name}" for handler in expected_handler_order]
                expected_shared_called_order.extend(calls)
        else:
            for handler in expected_handler_order:
                calls = [f"{handler} {item.go.name}" for item in items]
                expected_shared_called_order.extend(calls)

        if debug:
            print("Expected shared called order:")
            print(expected_shared_called_order)

            print()
            print("Shared called order:")
            print(self.called_order)

        assert self.called_order == expected_shared_called_order
