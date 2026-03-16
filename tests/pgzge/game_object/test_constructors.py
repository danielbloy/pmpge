import pytest

from pgzge.core import GameObject
from tests.pgzge.game_object.test_utilities import TestHandlers


def validate_properties(
        go: GameObject,
        name: str | None = None,
        active=True,
        enabled=True,
        visible=True,
        destroyed=False,
        parent=None,
        children=None):
    """
    Validate the properties of the GameObject class.
    """

    if children is None:
        children = []

    assert go.name is name
    assert go.active is active
    assert go.enabled is enabled
    assert go.visible is visible
    assert go.destroyed is destroyed
    assert go.parent is parent
    assert go.children == children


class TestGameObjectConstructors:
    """
    This suite of tests is to validate the GameObject constructor with its
    many optional arguments.
    """

    def test_empty_constructor(self):
        """
        Validate the default GameObject state.
        """
        go = GameObject()
        validate_properties(go)

    def test_name(self):
        """
        Validate that the name property is set correctly.
        """
        go = GameObject(name="test")
        validate_properties(go, name="test")

        go = GameObject(name="daniel.bloy")
        validate_properties(go, name="daniel.bloy")

    def test_activate_is_called(self):
        """
        Validate that the activate handler is called when the GameObject is constructed.
        """
        go = GameObject()
        validate_properties(go)

        handlers = TestHandlers()
        go = GameObject(
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate)

        validate_properties(go)
        handlers.validate(activate=go, activate_count=1)

    def test_deactivate_is_called(self):
        """
        Validate that the deactivate handler is called when the GameObject is constructed.
        """
        go = GameObject(active=False)
        validate_properties(go, active=False)

        handlers = TestHandlers()
        go = GameObject(
            active=False,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate)

        validate_properties(go, active=False)
        handlers.validate(deactivate=go, deactivate_count=1)

    def test_enabled(self):
        """
        Validate that the enabled property is set correctly.
        """
        go = GameObject(enabled=True)
        validate_properties(go, enabled=True)

        go = GameObject(enabled=False)
        validate_properties(go, enabled=False)

    def test_visible(self):
        """
        Validate that the visible property is set correctly.
        """
        go = GameObject(visible=True)
        validate_properties(go, visible=True)

        go = GameObject(visible=False)
        validate_properties(go, visible=False)

    def test_parent(self):
        """
        Validate that the parent property is set correctly. More complex test are done in
        test_parent_and_children.py.
        """
        parent = GameObject("parent")
        go = GameObject(parent=parent)
        validate_properties(go, parent=parent)
        assert parent.children == [go]

    def test_single_child(self):
        """
        Validate that the children property is set correctly. This also does a basic test
        of propagating the active and deactivate handlers to children.
        """
        # Active/active, no handler called
        child1_handlers = TestHandlers()
        child1 = GameObject(
            activate_handler=child1_handlers.activate,
            deactivate_handler=child1_handlers.deactivate)
        child1_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="parent", children=[child1],
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate)

        validate_properties(go, name="parent", children=[child1])
        handlers.validate(activate=go, activate_count=1)

        assert child1.parent == go
        child1_handlers.validate()

        # Deactivate/activate, handler called
        child1_handlers = TestHandlers()
        child1 = GameObject(
            active=False,
            activate_handler=child1_handlers.activate,
            deactivate_handler=child1_handlers.deactivate)
        child1_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="parent", children=[child1],
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate)

        validate_properties(go, name="parent", children=[child1], )
        handlers.validate(activate=go, activate_count=1)

        assert child1.parent == go
        child1_handlers.validate(activate=child1, activate_count=1)

        # Activate/deactivate, handler called
        child1_handlers = TestHandlers()
        child1 = GameObject(
            activate_handler=child1_handlers.activate,
            deactivate_handler=child1_handlers.deactivate)
        child1_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="parent", active=False, children=[child1],
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate)

        validate_properties(go, name="parent", active=False, children=[child1])
        handlers.validate(deactivate=go, deactivate_count=1)

        assert child1.parent == go
        child1_handlers.validate(deactivate=child1, deactivate_count=1)

    def test_multiple_children(self):
        """
        Validate that multiple children can be set at once. This also validates that the
        activate/deactivate handlers are called on the children correctly too.
        """
        child1_handlers = TestHandlers()
        child1 = GameObject(
            active=False,
            activate_handler=child1_handlers.activate,
            deactivate_handler=child1_handlers.deactivate)
        child1_handlers.reset()

        child2_handlers = TestHandlers()
        child2 = GameObject(
            active=True,
            activate_handler=child2_handlers.activate,
            deactivate_handler=child2_handlers.deactivate)
        child2_handlers.reset()

        child3_handlers = TestHandlers()
        child3 = GameObject(
            active=False,
            activate_handler=child3_handlers.activate,
            deactivate_handler=child3_handlers.deactivate)
        child3_handlers.reset()

        handlers = TestHandlers()
        go = GameObject(name="another parent", children=[child1, child2, child3],
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate)

        validate_properties(go, name="another parent",
                            children=[child1, child2, child3])
        handlers.validate(activate=go, activate_count=1)

        assert child1.parent == go
        child1_handlers.validate(activate=child1, activate_count=1)

        assert child2.parent == go
        child2_handlers.validate()

        assert child3.parent == go
        child3_handlers.validate(activate=child3, activate_count=1)

    def test_children_list_is_copied(self):
        """
        This ensures that if the list passed in containing the children is mutated, it
        does not affect parent objects child list.
        """
        # Construct the children and parent.
        child1 = GameObject(name="child1")
        child2 = GameObject(name="child2")
        child3 = GameObject(name="child3")
        children = [child1, child2, child3]
        go = GameObject(name="parent", children=children)

        validate_properties(go, name="parent", children=[child1, child2, child3])

        # Now we modify the original list passed in.
        child4 = GameObject(name="child4")
        children.remove(child1)
        children.append(child4)

        # Now validate the parent GameObject has not changed.
        validate_properties(go, name="parent", children=[child1, child2, child3])

    def test_combination_of_properties(self):
        """
        Validate that multiple properties can be set at once.
        """
        child1 = GameObject(name="child1")
        handlers = TestHandlers()
        go = GameObject(name="frank", enabled=True, visible=False, active=True,
                        children=[child1],
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate)

        validate_properties(go, name="frank", enabled=True, visible=False, active=True,
                            children=[child1])
        handlers.validate(activate=go, activate_count=1)
        assert child1.parent == go

        handlers.reset()
        child1 = GameObject(name="child1")
        child2 = GameObject(name="child2")
        child3 = GameObject(name="child3")
        go = GameObject(name="rob", enabled=False, visible=True, active=False,
                        children=[child1, child2, child3],
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate)

        validate_properties(go, name="rob", enabled=False, visible=True, active=False,
                            children=[child1, child2, child3])
        handlers.validate(deactivate=go, deactivate_count=1)
        assert child1.parent == go
        assert child2.parent == go
        assert child3.parent == go

    def test_no_other_handlers_called(self):
        """
        Validate that no other handlers are called when the GameObject is constructed.
        """
        handlers = TestHandlers()
        go = GameObject(
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.validate(activate=go, activate_count=1)

    def test_try_to_add_child_with_parent(self):
        """
        This trys to add a child that already has a parent (it should error).
        """
        child1 = GameObject(name="child1")
        child2 = GameObject(name="child2")

        parent1 = GameObject(name="parent1", children=[child2])

        with pytest.raises(ValueError):
            parent2 = GameObject(name="parent2", children=[child1, child2])

    def test_draw_handler_called(self):
        """
        This is a basic test that ensures the draw handler is called.
        """
        handlers = TestHandlers()
        go = GameObject(draw_handler=handlers.draw,
                        update_handler=handlers.update,
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate,
                        destroy_handler=handlers.destroy)

        handlers.validate(activate=go, activate_count=1)
        handlers.reset()

        go.draw_hierarchy("surface")
        handlers.validate(draw=(go, "surface"), draw_count=1)

    def test_update_handler_called(self):
        """
        This is a basic test that ensures the update handler is called.
        """
        handlers = TestHandlers()
        go = GameObject(draw_handler=handlers.draw,
                        update_handler=handlers.update,
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate,
                        destroy_handler=handlers.destroy)

        handlers.validate(activate=go, activate_count=1)
        handlers.reset()

        go.update_hierarchy(0.1)
        handlers.validate(update=(go, 0.1), update_count=1)

    def test_destroy_handler_called(self):
        """
        This is a basic test that ensures the destroy handler is called.
        """
        handlers = TestHandlers()
        go = GameObject(draw_handler=handlers.draw,
                        update_handler=handlers.update,
                        activate_handler=handlers.activate,
                        deactivate_handler=handlers.deactivate,
                        destroy_handler=handlers.destroy)

        handlers.validate(activate=go, activate_count=1)
        handlers.reset()

        go.destroy()  # This will also deactivate the GameObject
        handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1)

    def test_activate_draw_update_deactivate_destroy_handlers_called(self):
        """
        This is a basic test that ensures all the handlers are called.
        """
        handlers = TestHandlers()
        go = GameObject(
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.validate(activate=go, activate_count=1)

        handlers.reset()
        go.draw_hierarchy("surface")
        handlers.validate(draw=(go, "surface"), draw_count=1)

        handlers.reset()
        go.update_hierarchy(0.1)
        handlers.validate(update=(go, 0.1), update_count=1)

        handlers.reset()
        go.destroy()  # This will also deactivate the GameObject
        handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1)

    def test_multiple_activate_handlers_called(self):
        """
        This is a basic test that ensures multiple activate handlers are called.
        We also test that all handlers are merged into a single list.
        """
        handlers = TestHandlers()
        handlers1 = TestHandlers()
        handlers2 = TestHandlers()
        go = GameObject(
            activate_handlers=[handlers1.activate, handlers2.activate, handlers2.activate],
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.validate(activate=go, activate_count=1)
        handlers1.validate(activate=go, activate_count=1)
        handlers2.validate(activate=go, activate_count=2)

    def test_multiple_deactivate_handlers_called(self):
        """
        This is a basic test that ensures multiple deactivate handlers are called.
        We also test that all handlers are merged into a single list.
        """
        handlers = TestHandlers()
        handlers1 = TestHandlers()
        handlers2 = TestHandlers()
        go = GameObject(
            active=False,
            deactivate_handlers=[handlers1.deactivate, handlers2.deactivate, handlers2.deactivate],
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.validate(deactivate=go, deactivate_count=1)
        handlers1.validate(deactivate=go, deactivate_count=1)
        handlers2.validate(deactivate=go, deactivate_count=2)

    def test_multiple_draw_handlers_called(self):
        """
        This is a basic test that ensures multiple draw handlers are called.
        We also test that all handlers are merged into a single list.
        """
        handlers = TestHandlers()
        handlers1 = TestHandlers()
        handlers2 = TestHandlers()
        go = GameObject(
            draw_handlers=[handlers1.draw, handlers2.draw, handlers2.draw],
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.reset()
        go.draw_hierarchy("surface")
        handlers.validate(draw=(go, "surface"), draw_count=1)
        handlers1.validate(draw=(go, "surface"), draw_count=1)
        handlers2.validate(draw=(go, "surface"), draw_count=2)

    def test_multiple_update_handlers_called(self):
        """
        This is a basic test that ensures the update handler is called.
        We also test that all handlers are merged into a single list.
        """
        handlers = TestHandlers()
        handlers1 = TestHandlers()
        handlers2 = TestHandlers()
        go = GameObject(
            update_handlers=[handlers1.update, handlers2.update, handlers2.update],
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.reset()
        go.update_hierarchy(0.1)
        handlers.validate(update=(go, 0.1), update_count=1)
        handlers1.validate(update=(go, 0.1), update_count=1)
        handlers2.validate(update=(go, 0.1), update_count=2)

    def test_multiple_destroy_handlers_called(self):
        """
        This is a basic test that ensures the destroy handler is called.
        We also test that all handlers are merged into a single list.
        """
        handlers = TestHandlers()
        handlers1 = TestHandlers()
        handlers2 = TestHandlers()
        go = GameObject(
            destroy_handlers=[handlers1.destroy, handlers2.destroy, handlers2.destroy],
            draw_handler=handlers.draw,
            update_handler=handlers.update,
            activate_handler=handlers.activate,
            deactivate_handler=handlers.deactivate,
            destroy_handler=handlers.destroy)

        handlers.reset()
        go.destroy()  # This will also deactivate the GameObject
        handlers.validate(deactivate=go, deactivate_count=1, destroy=go, destroy_count=1)
        handlers1.validate(destroy=go, destroy_count=1)
        handlers2.validate(destroy=go, destroy_count=2)

    def test_validate_handlers_copied(self):
        """
        This ensures that the lists of handlers passed in is copied so the calling
        code cannot mutate it later.
        """
        handlers = TestHandlers()
        activate_handlers = [handlers.activate, handlers.activate, handlers.activate]
        deactivate_handlers = [handlers.deactivate, handlers.deactivate, handlers.deactivate]
        draw_handlers = [handlers.draw, handlers.draw, handlers.draw]
        update_handlers = [handlers.update, handlers.update, handlers.update]
        destroy_handlers = [handlers.destroy, handlers.destroy, handlers.destroy]

        go = GameObject(
            active=False,
            activate_handlers=activate_handlers,
            deactivate_handlers=deactivate_handlers,
            draw_handlers=draw_handlers,
            update_handlers=update_handlers,
            destroy_handlers=destroy_handlers)

        handlers.validate(deactivate=go, deactivate_count=3)

        # Modify the original list by adding another handler. This should not impact
        # the GameObject instance go.
        activate_handlers.append(handlers.activate)
        deactivate_handlers.append(handlers.deactivate)
        draw_handlers.append(handlers.draw)
        update_handlers.append(handlers.update)
        destroy_handlers.append(handlers.destroy)

        handlers.reset()
        go.activate()
        handlers.validate(activate=go, activate_count=3)

        handlers.reset()
        go.draw_hierarchy("surface")
        handlers.validate(draw=(go, "surface"), draw_count=3)

        handlers.reset()
        go.update_hierarchy(0.2)
        handlers.validate(update=(go, 0.2), update_count=3)

        handlers.reset()
        go.destroy()  # This will also deactivate the GameObject
        handlers.validate(deactivate=go, deactivate_count=3, destroy=go, destroy_count=3)
