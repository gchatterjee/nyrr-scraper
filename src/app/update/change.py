import json
from race import Race
from toString import (
    getDateChangeString,
    getLocationChangeString,
    getRaceChangedTitle,
    getStatusChangeString,
    getUrlString,
)
from update.update import Update, UpdateType


class Change(Update):
    def __init__(self, oldState: Race, newState: Race) -> None:
        super().__init__(newState, UpdateType.CHANGE)
        self.oldState = oldState

    def __str__(self) -> str:
        title = getRaceChangedTitle(self.state)
        templated = [
            getDateChangeString(self.oldState, self.state),
            getLocationChangeString(self.oldState, self.state),
            getStatusChangeString(self.oldState, self.state),
            getUrlString(self.state),
        ]
        phrases = [title]
        if templated.count(None) < len(templated):
            phrases.append("\n")
        for phrase in templated:
            if phrase is not None:
                phrases.append(phrase)
        return "<br/>".join(phrases)

    def __repr__(self) -> str:
        return json.dumps(
            {"type": self.type, "oldState": self.oldState, "state": self.state}
        )
