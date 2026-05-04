from pmpge.environment import is_running_on_desktop

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable
    from typing import Self, Any


class GameObject:
    """
    GameObject is the base class for all objects in the game. It provides a simple parent/child
    structure for updating and drawing GameObjects as well as a simple way to manage active and
    visible states.

    A GameObject has the following built-in properties:
        * name: The name of this object. Used when locating an object by name. Must not contain the
                `/` or `.` characters.
        * active: This has to be True for the GameObject to be updated or drawn (visible and
                  enabled also need to be True). The value of active is propagated to all children.
                  Changing active will also trigger the corresponding handlers.
        * alive: If this is False, the object will be removed from its parent at the next update.
                 Can only be set to False by calling destroy(). When set to False, the corresponding
                 handlers will be triggered and destroy will be propagated to all children.
        * enabled: If this is True and active is also True, the object will be updated. This is not
                   propagated to children. Enabled only ever impacts this GameObject, even during
                   updates (i.e. updates are still propagated to children even if this is False).
        * visible: If this is True and active is also True, the object will be drawn. This is not
                   propagated to children.
        * parent: The parent GameObject. This is None if the GameObject has no parent. A GameObject
                  can only have one parent. It is an error to add a GameObject as a child to
                  multiple parents.
        * children: A list of child GameObjects. These will be updated and drawn only if this
                    GameObject is active.

    A GameObject also provides a set of events that can have handlers attached to them. The handlers
    can be used to provide instance-specific behaviour without having to make a subclass and
    override one of the `draw()`, `update()`, `activate()`, `deactivate()` or destroyed() methods.
    These handlers are also used with Traits (see later).
        * draw_handlers: Draw handlers are called during `draw_hierarchy()` if the GameObject is
          active and visible.
        * update_handlers: Update handlers are called during `update_hierarchy()` if the GameObject
          is active and enabled.
        * activate_handlers = Activate handlers are called when active changes from False to True.
        * deactivate_handlers = Deactivate handlers are called when active changes from True to
          False.
        * destroy_handlers = Destroy handlers are called when `destroy()` is called on the
          GameObject.

    The `update_hierarchy()` and `draw_hierarchy()` methods propagate down the hierarchy if active
    is True and regardless of the visible and active properties (which only apply to this
    GameObject instance). i.e. a child can be enabled or visible even if the parent is not.

    Destroy, activate and deactivate are propagated to all children irrespective of whether
    active is True or False. All handlers are called before passing to the children except for
    destroy which propagates to the children first.

    The `draw()`, `update()`, `activate()`, `deactivate()` and destroyed() methods are called before
    any handlers.

    GameObjects can also have traits applied to them. Traits are a kind of Mixin and used as a way
    to apply behaviour to a GameObject without subclassing. Traits make use of the handlers. When a
    trait is "applied" to a GameObject, all variables are copied from the trait instance to the
    GameObject and if any of the following methods are present on the trait instance, they are copied
    across to the relevant handler too. This mechanism allows traits to depend on other traits and
    access the same state. Methods that are attached to the GameObjects handlers:
        * draw()
        * update()
        * activated()
        * deactivated()
        * destroyed()

    When a trait is "applied", it will have either the `activated()` or `deactivated()` method called
    based on the state of the GameObject. Finally, if a `merged()` method is present on the trait,
    that will be called.

    Traits are not a complete replacement for subclassing because the entire object is not copied across.
    For example, methods, property getter and setter methods. For an example of a subclass using traits,
    see the Sprite class.
    """
    __parent: Self | None
    __name: str | None
    __active: bool
    visible: bool
    enabled: bool
    __children: list[Self]
    __alive: bool

    __draw_handlers: list[Callable[[Self, Any], None]]
    __update_handlers: list[Callable[[Self, float], None]]
    __activate_handlers: list[Callable[[Self], None]]
    __deactivate_handlers: list[Callable[[Self], None]]
    __destroy_handlers: list[Callable[[Self], None]]

    def __init__(self,
                 *traits,
                 name: str | None = None,
                 active: bool = True,
                 enabled: bool = True,
                 visible: bool = True,
                 parent: Self | None = None,
                 children: list[Self] = None,
                 draw_handler: Callable[[Self, Any], None] = None,
                 update_handler: Callable[[Self, float], None] = None,
                 activate_handler: Callable[[Self], None] = None,
                 deactivate_handler: Callable[[Self], None] = None,
                 destroy_handler: Callable[[Self], None] = None,
                 draw_handlers: list[Callable[[Self, Any], None]] = None,
                 update_handlers: list[Callable[[Self, float], None]] = None,
                 activate_handlers: list[Callable[[Self], None]] = None,
                 deactivate_handlers: list[Callable[[Self], None]] = None,
                 destroy_handlers: list[Callable[[Self], None]] = None):
        """
        Initialises a GameObjects properties with the provided arguments. All arguments are optional
        and have a corresponding property. The only point of note is that the active property is set
        twice to force on of the activate() or deactivate() methods and corresponding events
        handlers to be called.
        """
        self.__parent = None
        self.__name = name
        self.visible = visible
        self.enabled = enabled
        self.__children = []
        self.__alive = True

        # Copy across the handler lists first; this creates empty lists if there are no
        # handler lists specified.
        self.__draw_handlers = draw_handlers.copy() if draw_handlers else []
        self.__update_handlers = update_handlers.copy() if update_handlers else []
        self.__activate_handlers = activate_handlers.copy() if activate_handlers else []
        self.__deactivate_handlers = deactivate_handlers.copy() if deactivate_handlers else []
        self.__destroy_handlers = destroy_handlers.copy() if destroy_handlers else []

        # Now add the individual handlers.
        self.__draw_handlers.append(draw_handler) if draw_handler else None
        self.__update_handlers.append(update_handler) if update_handler else None
        self.__activate_handlers.append(activate_handler) if activate_handler else None
        self.__deactivate_handlers.append(deactivate_handler) if deactivate_handler else None
        self.__destroy_handlers.append(destroy_handler) if destroy_handler else None

        # Now add the parent and children before the activate or deactivate events.
        if parent:
            parent.add_child(self)

        if children:
            for child in children:
                self.add_child(child)

        # This forces the active or deactivate events to be called.
        self.__active: bool = not active
        self.active = active

        # Add in the traits after triggering the active or deactivate events. This has to be
        # done here as we need the active state to determine which trait methods to call.
        for trait in traits:
            self.apply_trait(trait)

    @property
    def name(self) -> str | None:
        """
        The name of this GameObject or None if the GameObject has no name. It should not contain the
        `/` or `.`` characters. It is used when locating an object by name.

        :return: The name of this GameObject or None if the GameObject has no name.
        """
        return self.__name

    @property
    def active(self) -> bool:
        """"
        Returns whether the GameObject is active or not.
        """
        return self.__active

    @active.setter
    def active(self, value: bool) -> None:
        """
        Setting active to True or False will activate or deactivate the object (only if the new
        active state is different to the current active state). The active value is propagated to
        all children. In the case where this object is `destroyed` then no action is taken.
        """
        # Cannot activate a destroyed GameObject.
        if not self.__alive:
            return

        do_handlers = self.__active != value

        self.__active = value

        if do_handlers:
            if value:
                self.activated()
                for handler in self.__activate_handlers:
                    handler(self)
            else:
                self.deactivated()
                for handler in self.__deactivate_handlers:
                    handler(self)

        # Propagate the active state to all children.
        for child in self.__children:
            child.active = value

    def activated(self) -> None:
        """
        This is called when the GameObject is activated. It provides an easy way for subclasses to
        provide activation code without using handlers.
        """
        pass

    def deactivated(self) -> None:
        """
        This is called when the GameObject is deactivated. It provides an easy way for subclasses to
        provide deactivation code without using handlers.
        """
        pass

    def activate(self) -> Self:
        """
        Activates the GameObject. This will trigger the activate handlers and propagate the active
        state to all children. This is a shorthand version of `self.active = True` but also returns
        the GameObject.
        """
        self.active = True
        return self

    def deactivate(self) -> Self:
        """
        Deactivates the GameObject. This will trigger the deactivate handlers and propagate the
        active state to all children. This is a shorthand version of `self.active = False` but also
        returns the GameObject.
        """
        self.active = False
        return self

    def reset(self) -> Self:
        """
        Convenience method to toggle the active state of the GameObject to trigger the corresponding
        handlers. If the GameObject is active, it will be deactivated and then activated again. If
        the GameObject is deactivated, it will be activated and then deactivated again.
        """
        if self.active:
            self.deactivate().activate()
        else:
            self.activate().deactivate()

        return self

    @property
    def disabled(self) -> bool:
        """
        Returns whether this object is disabled or not. This is the opposite of enabled.
        """
        return not self.enabled

    @disabled.setter
    def disabled(self, value: bool) -> None:
        """
        Sets whether this object is disabled or not. This is the opposite of enabled.
        """
        self.enabled = not value

    @property
    def alive(self) -> bool:
        """
        Returns whether this object is alive or not. An alive object is not destroyed.
        """
        return self.__alive

    def destroy(self) -> None:
        """
        Destroys the object, propagating to all children before the handlers for this object are
        triggered. Starting from the leaf nodes, each object will be deactivated and then destroyed
        in turn; the sequence of events is thus:
         * deactivate child
         * destroy child
         * deactivate parent
         * destroy parent
        """

        # Propagate the deactivated state to all children.
        for child in self.__children:
            child.destroy()

        if not self.__alive:
            return

        self.deactivate()
        self.__alive = False

        self.destroyed()
        for handler in self.__destroy_handlers:
            handler(self)

    def destroyed(self) -> None:
        """
        This is called when the GameObject is destroyed. It provides an easy way for subclasses to
        provide destruction code without using handlers.
        """
        pass

    @property
    def parent(self) -> Self | None:
        """
        The parent GameObject or None if this GameObject has no parent.
        """
        return self.__parent

    @property
    def children(self) -> list[Self]:
        """
        Returns all the children of this GameObject. If there are no children, an empty list
        is returned.
        """
        return self.__children.copy()

    def add_child(self, child: Self) -> Self:
        """
        Adds a GameObject as a child of this GameObject. If the child object already has a parent an
        error will be raised. This will set the parent of the child to this GameObject.
        """
        if not child:
            return self

        if child.__parent:
            if child.__parent == self:
                return self

            raise ValueError("child already has a parent")

        child.__parent = self
        self.__children.append(child)
        return self

    def remove_child(self, child: Self) -> Self:
        """
        Removes a GameObject as a child of this GameObject. If the childs parent is not this
        GameObject then an error will be raised (an exception to this is if the child has no
        parent).
        """
        # If this child does not have a parent, ignore.
        if not child or not child.__parent:
            return self

        if child.__parent != self:
            raise ValueError("child is not a child of this GameObject")

        child.__parent = None
        self.__children.remove(child)
        return self

    def traverse_hierarchy(self, func: Callable[[Self, Any], tuple[bool, Any]], initial_state: Any = None) -> Self:
        """
        Provides a way to traverse the entire hierarchy, executing a function on
        each node and passing state. The `func` accepts two parameters:
        * The GameObject instance.
        * Some state (which can be `None`).

        The `func` returns two values:
        * A boolean indicating whether to process nodes children or not.
        * A new value for state to be passed to the children (which can be `None`)

        The GameObject that `traverse_hierarchy` is called on is always processed.
        """

        def process(go: Self, state: Any):
            process_children, new_state = func(go, state)
            if process_children:
                for child in go.__children:
                    process(child, new_state)

        process(self, initial_state)
        return self

    def draw_hierarchy(self, surface: Any) -> Self:
        """
        Draws the GameObject (if `active` and `visible`) and propagates to children (if `active`).
        The surface is passed down through all objects but does not need to be a Pygame surface.
        This doesn't use traverse_hierarchy as it is slower.
        """
        if not self.active:
            return self

        if self.visible:
            self.draw(surface)
            for handler in self.__draw_handlers:
                handler(self, surface)

        for child in self.__children:
            child.draw_hierarchy(surface)

        return self

    def draw(self, surface: Any) -> None:
        """
        This is called when the GameObject is drawn. It provides an easy way for subclasses to
        provide draw code without using handlers and without having to remember to call the
        superclass.
        """
        pass

    def update_hierarchy(self, dt: float) -> Self:
        """
        Updates the GameObject (if `active` and `enabled`) and propagates to children (if `active`).
        Also removes any destroyed children. This doesn't use traverse_hierarchy as it is slower.
        """
        # Remove any destroyed children.
        children = self.__children
        for child in children:
            if not child.__alive:
                child.__parent = None
                children.remove(child)

        if not self.active:
            return self

        if self.enabled:
            self.update(dt)
            for handler in self.__update_handlers:
                handler(self, dt)

        for child in self.__children:
            child.update_hierarchy(dt)

        return self

    def update(self, dt: float) -> None:
        """
        This is called when the GameObject is updated. It provides an easy way for subclasses to
        provide update code without using handlers and without having to remember to call the
        superclass.
        """
        pass

    def add_draw_handler(self, handler: Callable[[Self, Any], None]) -> Self:
        """Adds a `draw` handler."""
        # noinspection PyTypeChecker
        self.__draw_handlers.append(handler) if handler else None
        return self

    def remove_draw_handler(self, handler: Callable[[Self, Any], None]) -> Self:
        """Removes a `draw` handler."""
        if handler and handler in self.__draw_handlers:
            # noinspection PyTypeChecker
            self.__draw_handlers.remove(handler)
        return self

    def add_update_handler(self, handler: Callable[[Self, float], None]) -> Self:
        """Adds a `update` handler."""
        # noinspection PyTypeChecker
        self.__update_handlers.append(handler) if handler else None
        return self

    def remove_update_handler(self, handler: Callable[[Self, float], None]) -> Self:
        """Removes a `update` handler."""
        if handler and handler in self.__update_handlers:
            # noinspection PyTypeChecker
            self.__update_handlers.remove(handler)
        return self

    def add_activate_handler(self, handler: Callable[[Self], None]) -> Self:
        """Adds a `activate` handler."""
        # noinspection PyTypeChecker
        self.__activate_handlers.append(handler) if handler else None
        return self

    def remove_activate_handler(self, handler: Callable[[Self], None]) -> Self:
        """Removes a `activate` handler."""
        if handler and handler in self.__activate_handlers:
            # noinspection PyTypeChecker
            self.__activate_handlers.remove(handler)
        return self

    def add_deactivate_handler(self, handler: Callable[[Self], None]) -> Self:
        """Adds a `deactivate` handler."""
        # noinspection PyTypeChecker
        self.__deactivate_handlers.append(handler) if handler else None
        return self

    def remove_deactivate_handler(self, handler: Callable[[Self], None]) -> Self:
        """Removes a `deactivate` handler."""
        if handler and handler in self.__deactivate_handlers:
            # noinspection PyTypeChecker
            self.__deactivate_handlers.remove(handler)
        return self

    def add_destroy_handler(self, handler: Callable[[Self], None]) -> Self:
        """Adds a `destroy` handler."""
        # noinspection PyTypeChecker
        self.__destroy_handlers.append(handler) if handler else None
        return self

    def remove_destroy_handler(self, handler: Callable[[Self], None]) -> Self:
        """Removes a `destroy` handler."""
        if handler and handler in self.__destroy_handlers:
            # noinspection PyTypeChecker
            self.__destroy_handlers.remove(handler)
        return self

    not_allowed_attributes = ['draw', 'update', 'activated', 'deactivated', 'destroyed', 'merged']

    def apply_trait(self, trait: Any) -> Self:
        """
        Merge the properties and handlers of a trait object into this GameObject. It will
        not merge across methods or property getter and setters. For that you will need to
        define a subclass of GameObject.

        When a trait is "applied", it will have either the `activated()` or `deactivated()`
        method called based on the state of the GameObject.

        Finally, if a `merged()` method is present on the trait, that will be called.
        """
        if isinstance(trait, type):
            trait.__init__(self)
            cls = trait
        else:
            # Copy across attributes
            for attribute in dir(trait):
                if attribute.startswith('__') or attribute in GameObject.not_allowed_attributes:
                    continue
                setattr(self, attribute, getattr(trait, attribute))
            cls = trait.__class__

        if hasattr(cls, 'draw'):
            self.add_draw_handler(cls.draw)

        if hasattr(cls, 'update'):
            self.add_update_handler(cls.update)

        if hasattr(cls, 'activated'):
            self.add_activate_handler(cls.activated)

        if hasattr(cls, 'deactivated'):
            self.add_deactivate_handler(cls.deactivated)

        if hasattr(cls, 'destroyed'):
            self.add_destroy_handler(cls.destroyed)

        # Trigger activate and/or deactivate handlers on the combined game_object if they exist.
        if hasattr(cls, 'activated') and self.active:
            cls.activated(self)

        if hasattr(cls, 'deactivated') and not self.active:
            cls.deactivated(self)

        # Finally trigger the merge handler.
        if hasattr(cls, 'merged'):
            cls.merged(self)

        return self
