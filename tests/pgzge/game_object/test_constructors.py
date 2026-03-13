from pgzge.core import GameObject
from tests.pgzge.game_object.test_utilities import TestHandlers


class TestGameObjectConstructors:
    """
    This suite of tests is to validate the GameObject constructor with its
    many optional arguments.
    """

    @staticmethod
    def validate_properties(
            go: GameObject,
            name: str | None = None,
            active=True,
            enabled=True,
            visible=True,
            destroyed=False,
            parent=None,
            children=None):
        if children is None:
            children = []

        assert go.name is name
        assert go.active is active
        assert go.enabled is enabled
        assert go.visible is visible
        assert go.destroyed is destroyed
        assert go.parent is parent
        assert go.children == children

    def test_empty_constructor(self):
        """
        Validate the default GameObject state.
        """
        go = GameObject()
        self.validate_properties(go)

    def test_name(self):
        """
        Validate that the name property is set correctly.
        """
        go = GameObject(name="test")
        self.validate_properties(go, name="test")

        go = GameObject(name="daniel.bloy")
        self.validate_properties(go, name="daniel.bloy")

    def test_activate_is_called(self):
        """
        Validate that the activate handler is called when the GameObject is constructed.
        """
        go = GameObject()
        self.validate_properties(go)

        handlers = TestHandlers()
        go = GameObject(
            activate_handler=lambda obj: handlers.activate(obj),
            deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go)
        assert handlers.activate_called == go
        assert handlers.activate_called_count == 1
        assert handlers.deactivate_called is None

    def test_deactivate_is_called(self):
        """
        Validate that the deactivate handler is called when the GameObject is constructed.
        """
        go = GameObject(active=False)
        self.validate_properties(go, active=False)

        handlers = TestHandlers()
        go = GameObject(
            active=False,
            activate_handler=lambda obj: handlers.activate(obj),
            deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go, active=False)
        assert handlers.activate_called is None
        assert handlers.deactivate_called is go
        assert handlers.deactivate_called_count == 1

    def test_enabled(self):
        """
        Validate that the enabled property is set correctly.
        """
        go = GameObject(enabled=True)
        self.validate_properties(go, enabled=True)

        go = GameObject(enabled=False)
        self.validate_properties(go, enabled=False)

    def test_visible(self):
        """
        Validate that the visible property is set correctly.
        """
        go = GameObject(visible=True)
        self.validate_properties(go, visible=True)

        go = GameObject(visible=False)
        self.validate_properties(go, visible=False)

    def test_parent(self):
        """
        Validate that the parent property is set correctly. More complex test are done in
        test_parent_and_children.py.
        """
        parent = GameObject("parent")
        go = GameObject(parent=parent)
        self.validate_properties(go, parent=parent)
        assert parent.children == [go]

    def test_single_child(self):
        """
        Validate that the children property is set correctly. This also does a basic test
        of propagating the active and deactivate handlers to children.
        """
        # Active/active, no handler called
        child1_handlers = TestHandlers()
        child1 = GameObject(
            activate_handler=lambda obj: child1_handlers.activate(obj),
            deactivate_handler=lambda obj: child1_handlers.deactivate(obj))
        child1_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="parent", children=[child1],
                        activate_handler=lambda obj: handlers.activate(obj),
                        deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go, name="parent", children=[child1])
        assert handlers.activate_called == go
        assert handlers.activate_called_count == 1
        assert handlers.deactivate_called is None

        assert child1.parent == go
        assert child1_handlers.activate_called is None
        assert child1_handlers.deactivate_called is None

        # Deactive/active, handler called
        child1_handlers = TestHandlers()
        child1 = GameObject(
            active=False,
            activate_handler=lambda obj: child1_handlers.activate(obj),
            deactivate_handler=lambda obj: child1_handlers.deactivate(obj))
        child1_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="parent", children=[child1],
                        activate_handler=lambda obj: handlers.activate(obj),
                        deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go, name="parent", children=[child1], )
        assert handlers.activate_called == go
        assert handlers.activate_called_count == 1
        assert handlers.deactivate_called is None

        assert child1.parent == go
        assert child1_handlers.activate_called is child1
        assert child1_handlers.activate_called_count == 1
        assert child1_handlers.deactivate_called is None

        # Active/deactive, handler called
        child1_handlers = TestHandlers()
        child1 = GameObject(
            activate_handler=lambda obj: child1_handlers.activate(obj),
            deactivate_handler=lambda obj: child1_handlers.deactivate(obj))
        child1_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="parent", active=False, children=[child1],
                        activate_handler=lambda obj: handlers.activate(obj),
                        deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go, name="parent", active=False, children=[child1])
        assert handlers.activate_called is None
        assert handlers.deactivate_called is go
        assert handlers.deactivate_called_count == 1
        
        assert child1.parent == go
        assert child1_handlers.activate_called is None
        assert child1_handlers.deactivate_called is child1
        assert child1_handlers.deactivate_called_count == 1

    def test_multiple_children(self):
        """
        Validate that multiple children can be set at once.
        """
        child1 = GameObject()
        child2 = GameObject()
        go = GameObject(name="another parent", children=[child1, child2])
        self.validate_properties(go, name="another parent", children=[child1, child2])
        assert child1.parent == go
        assert child2.parent == go

        # TODO: Test that activate and deactivate propagate through to children at construction time.

    def test_combination_of_properties(self):
        """
        Validate that multiple properties can be set at once.
        """
        # TODO: Add parent and children to this test.
        handlers = TestHandlers()
        go = GameObject(name="frank", enabled=True, visible=False, active=True,
                        activate_handler=lambda obj: handlers.activate(obj),
                        deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go, name="frank", enabled=True, visible=False, active=True)
        assert handlers.activate_called == go
        assert handlers.activate_called_count == 1
        assert handlers.deactivate_called is None

        handlers.reset()
        go = GameObject(name="rob", enabled=False, visible=True, active=False,
                        activate_handler=lambda obj: handlers.activate(obj),
                        deactivate_handler=lambda obj: handlers.deactivate(obj))

        self.validate_properties(go, name="rob", enabled=False, visible=True, active=False)
        assert handlers.activate_called is None
        assert handlers.deactivate_called is go
        assert handlers.deactivate_called_count == 1

    def test_no_other_handlers_called(self):
        """
        Validate that no other handlers are called when the GameObject is constructed.
        """
        handlers = TestHandlers()
        go = GameObject(
            draw_handler=lambda obj, surface: handlers.draw(obj, surface),
            update_handler=lambda obj, dt: handlers.update(obj, dt),
            activate_handler=lambda obj: handlers.activate(obj),
            deactivate_handler=lambda obj: handlers.deactivate(obj),
            destroy_handler=lambda obj: handlers.destroy(obj))

        assert handlers.draw_called is None
        assert handlers.update_called is None
        assert handlers.activate_called == go
        assert handlers.activate_called_count == 1
        assert handlers.deactivate_called is None
        assert handlers.destroy_called is None

    # TODO: Simple validation of draw handler
    # TODO: Simple validation of update handler
    # TODO: Simple validation of destroy handler

    # TODO: Validate multiple activate and deactivate handlers get called.
    # TODO: Validate a list of handlers and an individual handler can be passed together.

    # TODO: Validate children cannot be changed through property or modifying list
    # TODO: Validate each of the other handlers work.
