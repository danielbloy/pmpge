# TODO: Document this and give considerable thought to how we can manage controllers
#       across all device types.
class Controller:

    @property
    def button_count(self):
        return 0

    @property
    def start(self) -> bool:
        return False

    @property
    def select(self) -> bool:
        return False

    @property
    def action(self) -> bool:
        return False

    @property
    def cancel(self) -> bool:
        return False
