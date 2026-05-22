print("No graphics driver")


def draw(screen):
    """
    Mandatory draw method, does nothing.
    """
    pass


def game_object_hierarchy_changed():
    """
    Mandatory function, does nothing.
    """
    pass


class DriverImageResource:
    """
    Mandatory class, does nothing.
    """

    def load(self, image: str) -> tuple[int, int]:
        return 0, 0


class GraphicsDrawImageTrait:
    """
    Mandatory class, does nothing.
    """
    pass
