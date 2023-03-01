from enum import Enum
import json
from race import Race


class UpdateType(Enum):
    ADDITION = "addition"
    REMOVAL = "removal"
    CHANGE = "change"


class Update:
    def __init__(
        self,
        state: Race,
        type: UpdateType,
    ) -> None:
        self.state = state
        self.type = type

    def __repr__(self) -> str:
        return json.dumps(
            {"type": self.type.value, "state": json.loads(self.state.__repr__())}
        )
