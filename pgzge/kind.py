# TODO: Temporary holding place for Kinds
from pgzge.core import new_kind


class Kinds:
    def __init__(self):
        self.types: dict[str, type] = {}

    def new(self, name: str, *traits_classes: type) -> type:
        if name in self.types:
            raise ValueError(f"Sprite kind '{name}' already exists.")

        self.types[name] = new_kind(name, *traits_classes)
        return self.types[name]

    def __contains__(self, item) -> bool:
        return item in self.types

    def __getitem__(self, item: str) -> type:
        return self.get(item)

    def __iter__(self):
        return iter(self.types.items())

    def get(self, name: str, *traits_classes: type) -> type:
        if name in self.types:
            return self.types[name]

        return self.new(name, *traits_classes)
