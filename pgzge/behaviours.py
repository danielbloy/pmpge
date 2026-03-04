class Behaviour:
    # TODO: Should it have an activate and deactivate handler?
    def enabled(self, obj: GameObject) -> bool:
        return True

    def execute(self, dt, obj: GameObject):
        pass

    def remove(self, obj: GameObject) -> bool:
        return False

    def added(self, obj: GameObject):
        pass

    def removed(self, obj: GameObject):
        pass


class Behaviours:
    def __init__(self, *behaviours: Behaviour):

        self.behaviours: list[Behaviour] = list(behaviours)

    def add_behaviour(self: GameObject | Self, behaviour: Behaviour) -> GameObject | Self:
        # TODO: Remove behaviour?
        self.behaviours += behaviour,
        behaviour.added(self)
        return self

    def update(self: GameObject | Self, dt: float):
        # TODO: Remove handler to be called

        self.behaviours = [
            behaviour for behaviour in self.behaviours
            if not behaviour.remove(self)
        ]
        for behaviour in self.behaviours:
            if behaviour.enabled(self):
                behaviour.execute(dt, self)

    def merged(self: GameObject | Self):
        print("Merging behaviours")
        print(self.__class__.__name__)
        for behaviour in self.behaviours:
            behaviour.added(self)