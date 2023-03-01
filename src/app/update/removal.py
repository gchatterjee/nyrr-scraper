from race import Race
from toString import getRaceRemovedTitle
from update.update import Update, UpdateType


class Removal(Update):
    def __init__(self, state: Race) -> None:
        super().__init__(state, UpdateType.REMOVAL)

    def __str__(self) -> str:
        return getRaceRemovedTitle(self.state)
