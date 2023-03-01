from race import Race
from toString import (
    getRaceAddedTitle,
    getScheduleString,
    getStatusString,
    getUrlString,
)
from update.update import Update, UpdateType


class Addition(Update):
    def __init__(self, state: Race) -> None:
        super().__init__(state, UpdateType.ADDITION)

    def __str__(self) -> str:
        title = getRaceAddedTitle(self.state)
        templated = [
            getScheduleString(self.state),
            getStatusString(self.state),
            getUrlString(self.state),
        ]
        phrases = [title]
        if templated.count(None) < len(templated):
            phrases.append("\n")
        for phrase in templated:
            if phrase is not None:
                phrases.append(phrase)
        return "<br/>".join(phrases)
